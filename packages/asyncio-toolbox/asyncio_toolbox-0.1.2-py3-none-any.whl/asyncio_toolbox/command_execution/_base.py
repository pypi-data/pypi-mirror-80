import asyncio
import json
import signal
import sys
from asyncio import StreamReader
from asyncio.subprocess import DEVNULL, PIPE, STDOUT, create_subprocess_exec
from functools import partial
from pathlib import Path
from subprocess import CalledProcessError
from typing import List, Mapping, Optional, Sequence, Union

import attr

from .windows_command_wrapper import __WINDOWS_COMMAND_WRAPPER_PATH
from .._helpers import create_task, is_frozen, is_windows
from ..tempfile import TemporaryDirectory

__WINDOWS_COMMAND_WRAPPER_EXECUTABLE_DEFAULT: List[str] = [
    sys.executable,
    __WINDOWS_COMMAND_WRAPPER_PATH,
]
__WINDOWS_COMMAND_WRAPPER_EXECUTABLE = __WINDOWS_COMMAND_WRAPPER_EXECUTABLE_DEFAULT[:]


def set_windows_command_wrapper_args(args: Sequence[Union[str, Path]]):
    __WINDOWS_COMMAND_WRAPPER_EXECUTABLE[:] = [str(arg) for arg in args]


def get_windows_command_wrapper_args() -> List[str]:
    if (
        is_frozen
        and __WINDOWS_COMMAND_WRAPPER_EXECUTABLE
        == __WINDOWS_COMMAND_WRAPPER_EXECUTABLE_DEFAULT
    ):
        raise RuntimeError(
            "Running as frozen executable and set_windows_command_wrapper_args was not called."
        )
    return __WINDOWS_COMMAND_WRAPPER_EXECUTABLE[:]


@attr.s(slots=True, auto_attribs=True, kw_only=True, frozen=True)
class Command:
    _args: Sequence[Union[str, Path]] = attr.ib()
    env: Optional[Mapping[str, str]] = None
    cwd: Optional[Union[str, Path]] = None

    merge_outputs: bool = False
    discard_stdout: bool = False
    discard_stderr: bool = False

    @property
    def args(self) -> Sequence[str]:
        return [str(arg) for arg in self._args]


@attr.s(slots=True)
class Process:
    process: asyncio.subprocess.Process = attr.ib()
    command: Command = attr.ib()

    stdout: List[str] = attr.ib(factory=list, init=False)
    _stdout_reader_task: Optional[asyncio.Task] = attr.ib(default=None, init=False)
    stderr: List[str] = attr.ib(factory=list, init=False)
    _stderr_reader_task: Optional[asyncio.Task] = attr.ib(default=None, init=False)

    _wait_process_task: Optional[asyncio.Task] = attr.ib(default=None, init=False)

    async def _store_stream(self, stream: StreamReader, storage: List[str]):
        while True:
            line = await stream.readline()
            if not line:
                return
            decoded_line = line.decode()
            storage.append(decoded_line.rstrip("\r\n"))
            if not decoded_line.endswith("\n"):
                return

    @classmethod
    async def _get_streams_config_from_command(cls, command):
        stdout = DEVNULL if command.discard_stdout else PIPE
        stderr = (
            DEVNULL
            if command.discard_stderr
            else STDOUT
            if command.merge_outputs
            else PIPE
        )
        return stderr, stdout

    async def start(self):
        if self.process.stdout is not None:
            self._stdout_reader_task = create_task(
                self._store_stream(self.process.stdout, self.stdout),
                name=f"process-{self.process.pid}-stdout-reader",
            )

        if self.process.stderr is not None:
            self._stderr_reader_task = create_task(
                self._store_stream(self.process.stderr, self.stderr),
                name=f"process-{self.process.pid}-stderr-reader",
            )

        self._wait_process_task = create_task(
            self.process.wait(), name=f"process-{self.process.pid}-waiter"
        )

    @property
    def pid(self) -> int:
        return self.process.pid

    @property
    def running(self) -> bool:
        return self.returncode is None

    @property
    def returncode(self) -> Optional[int]:
        return self.process.returncode

    async def interrupt(self) -> None:
        self.process.send_signal(signal=signal.SIGINT)
        await asyncio.sleep(0)

    async def kill(self) -> None:
        self.process.kill()
        await asyncio.sleep(0)

    async def terminate(self) -> None:
        self.process.terminate()
        await asyncio.sleep(0)

    async def wait(self, timeout: Optional[Union[float, int]] = None) -> int:
        if self._wait_process_task is None:
            raise ValueError("Process is not started")
        wait_task = asyncio.shield(self._wait_process_task)
        if timeout:
            return await asyncio.wait_for(wait_task, timeout)
        else:
            return await wait_task

    async def wait_for_all_workers(self):
        await asyncio.shield(
            asyncio.gather(
                *[
                    task
                    for task in [
                        self._wait_process_task,
                        self._stdout_reader_task,
                        self._stderr_reader_task,
                    ]
                    if task is not None
                ]
            )
        )
        return self.returncode

    @classmethod
    async def from_command(cls, command: Command) -> "Process":
        stderr, stdout = await cls._get_streams_config_from_command(command)
        process_handler = cls(
            process=await create_subprocess_exec(
                *command.args,
                stdin=DEVNULL,
                stdout=stdout,
                stderr=stderr,
                env=command.env,
                cwd=command.cwd,
            ),
            command=command,
        )
        await process_handler.start()
        return process_handler


if is_windows:
    from win32process import (
        CREATE_UNICODE_ENVIRONMENT,
        CREATE_NO_WINDOW,
    )

    @attr.s(slots=True, auto_attribs=True)
    class WinProcess(Process):
        _communication_dir: TemporaryDirectory = attr.ib()

        async def interrupt(self) -> None:
            await asyncio.get_event_loop().run_in_executor(
                None, (self._communication_dir.name / "INT").touch
            )

        # async def kill(self) -> None:
        #     await asyncio.get_event_loop().run_in_executor(
        #         None, (self._communication_dir.name / "KILL").touch
        #     )

        async def terminate(self) -> None:
            await asyncio.get_event_loop().run_in_executor(
                None, (self._communication_dir.name / "TERM").touch
            )

        kill = terminate

        async def _wait_for_wrapper_to_be_ready(self):
            def _thread_poller(
                ready_path: Path,
                error_path: Path,
                timeout: int = 10,
                polling_time: Union[int, float] = 0.1,
                process=asyncio.subprocess.Process,
            ):
                import time

                start_time = time.monotonic()
                while time.monotonic() - start_time <= timeout:
                    if ready_path.exists():
                        ready_path.unlink()
                        return
                    elif error_path.exists():
                        with error_path.open("rt") as f:
                            file_content = f.read()
                        error_path.unlink()
                        data = json.loads(file_content)
                        exception_type = data.pop("type")
                        if exception_type == "CalledProcessError":
                            raise CalledProcessError(**data)
                        elif exception_type == "OSError":
                            error = OSError()
                            error.errno = data["errno"]
                            error.strerror = data["strerror"]
                            raise error
                        else:
                            raise RuntimeError(
                                f"Process could no start for unknown reason {exception_type} : {data}"
                            )
                    elif process.returncode is not None:
                        return
                    else:
                        time.sleep(polling_time)

            await asyncio.get_event_loop().run_in_executor(
                None,
                partial(
                    _thread_poller,
                    ready_path=self._communication_dir.name / "READY",
                    error_path=self._communication_dir.name / "ERROR",
                    process=self.process,
                ),
            )

        @classmethod
        async def from_command(cls, command: Command) -> Process:
            stderr, stdout = await cls._get_streams_config_from_command(command)
            communication_dir = TemporaryDirectory(prefix="aiotoolbox_process_")
            await communication_dir.open()
            process_handler = cls(
                communication_dir=communication_dir,
                process=await create_subprocess_exec(
                    *get_windows_command_wrapper_args(),
                    str(communication_dir.name),
                    *command.args,
                    stdin=DEVNULL,
                    stdout=stdout,
                    stderr=stderr,
                    env=command.env,
                    cwd=command.cwd,
                    creationflags=CREATE_NO_WINDOW | CREATE_UNICODE_ENVIRONMENT,
                ),
                command=command,
            )
            await process_handler.start()
            await process_handler._wait_for_wrapper_to_be_ready()
            return process_handler

    Process = WinProcess  # type: ignore

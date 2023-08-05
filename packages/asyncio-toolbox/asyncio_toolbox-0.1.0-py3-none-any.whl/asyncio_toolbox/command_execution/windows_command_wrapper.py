from pathlib import Path
from typing import List

__WINDOWS_COMMAND_WRAPPER_PATH = __file__

# type: ignore
def wrap_windows_command_in_python_process(command: List[str], command_dir: Path):
    import os
    import signal
    import sys
    import time
    from contextlib import contextmanager
    import win32api

    from subprocess import Popen
    from threading import Thread
    from typing import Callable, Union, Dict

    # For PyInstaller
    exit = sys.exit

    # TODO: use this instead http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html

    @contextmanager
    def waiting_for_file(
        m: Dict[Path, Callable[[], None]], *, wait_time: Union[int, float] = 0.1
    ):
        stop = False

        def cb():
            while not stop:
                for path, action in m.items():
                    if path.exists():
                        path.unlink()
                        action()
                time.sleep(wait_time)

        t = Thread(target=cb)
        t.start()
        try:
            yield
        finally:
            stop = True
            t.join(2)

    sys_stdin = sys.stdin
    sys_stdout = sys.stdout
    sys_stderr = sys.stderr

    # CLear ctrl handlers
    win32api.SetConsoleCtrlHandler(None, True)
    win32api.SetConsoleCtrlHandler(None, False)

    try:
        p = Popen(command, stdin=sys_stdin, stdout=sys_stdout, stderr=sys_stderr)
    except OSError as we:
        with (command_dir / "ERROR").open("wt") as f:
            import json

            json.dump(dict(type="OSError", errno=we.errno, strerror=we.strerror), f)
        exit(-255)
    except BaseException as e:
        with (command_dir / "ERROR").open("wt") as f:
            import json

            json.dump(
                dict(
                    type="CalledProcessError",
                    returncode=-255,
                    cmd=command,
                    stderr=f"{e.__class__.__name__}:{e}",
                ),
                f,
            )
        exit(-255)
    else:
        # Ignore CTRL-C on this process
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGBREAK):  # type: ignore
            signal.signal(sig, signal.SIG_IGN)

        win32api.SetConsoleCtrlHandler(None, True)

        (command_dir / "READY").touch()

        with waiting_for_file(
            {
                command_dir / "INT": lambda: os.kill(0, signal.CTRL_C_EVENT),  # type: ignore
                command_dir / "KILL": lambda: os.kill(0, signal.CTRL_BREAK_EVENT),  # type: ignore
                command_dir / "TERM": p.terminate,
            },
        ):
            p.wait()
        return p.returncode


if __name__ == "__main__":
    import sys

    exit(wrap_windows_command_in_python_process(sys.argv[2:], Path(sys.argv[1])))

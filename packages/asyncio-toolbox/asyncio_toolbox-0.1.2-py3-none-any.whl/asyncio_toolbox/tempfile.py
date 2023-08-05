import asyncio
import tempfile
from functools import partial
from pathlib import Path
from typing import Optional, Union

import attr
from asyncio_toolbox._helpers import is_windows


if is_windows:
    import win32file


@attr.s(slots=True)
class TemporaryDirectory:
    suffix: Optional[str] = attr.ib(default=None)
    prefix: Optional[str] = attr.ib(default=None)
    dir: Optional[Union[str, Path]] = attr.ib(default=None)

    _temp_dir: Optional[tempfile.TemporaryDirectory] = attr.ib(default=None, init=False)

    @property
    def name(self) -> Path:
        if not self._temp_dir:
            raise ValueError(
                "Temporary directory not created, open() or __aenter__() must be called first"
            )
        if is_windows:
            return Path(win32file.GetLongPathName(self._temp_dir.name))
        else:
            return Path(self._temp_dir.name)

    async def open(self):
        if self._temp_dir is not None:
            raise ValueError(f"Temporary directory already opened")
        self._temp_dir = await asyncio.get_event_loop().run_in_executor(
            None,
            partial(
                tempfile.TemporaryDirectory,
                suffix=self.suffix,
                prefix=self.prefix,
                dir=self.dir,
            ),
        )

    async def close(self):
        if self._temp_dir is None:
            raise ValueError(f"Temporary directory is not opened")
        await asyncio.get_event_loop().run_in_executor(None, self._temp_dir.cleanup)
        self._temp_dir = None

    async def __aenter__(self):
        await self.open()
        return self.name

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

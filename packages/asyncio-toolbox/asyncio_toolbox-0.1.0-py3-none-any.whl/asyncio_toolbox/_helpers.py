import asyncio
import platform
import sys
from typing import Optional

is_windows = any(platform.win32_ver())
is_frozen = getattr(sys, "frozen", False)

if sys.version_info[:2] == (3, 6):

    def create_task(coro, *, name: Optional[str] = None):
        return asyncio.get_event_loop().create_task(coro)


else:

    def create_task(coro, *, name: Optional[str] = None):
        if sys.version_info[:2] >= (3, 8):
            create_task_kwargs = dict(name=name)
        else:
            create_task_kwargs = {}
        return asyncio.create_task(coro=coro, **create_task_kwargs)  # type: ignore

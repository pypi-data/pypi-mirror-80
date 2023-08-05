import asyncio
from typing import Generic, TypeVar

import typing_extensions


ITEM_T = TypeVar("ITEM_T")


class _Queue(typing_extensions.Protocol[ITEM_T]):
    async def put(self, item: ITEM_T):
        pass

    def put_nowait(self, item: ITEM_T):
        pass

    async def get(self) -> ITEM_T:
        pass

    def get_nowait(self) -> ITEM_T:
        pass


class Queue(Generic[ITEM_T], asyncio.Queue):
    async def put(self, item: ITEM_T) -> None:
        return await super().put(item)

    def put_nowait(self, item: ITEM_T) -> None:
        super().put_nowait(item)

    async def get(self) -> ITEM_T:
        return await super().get()

    def get_nowait(self) -> ITEM_T:
        return super().get_nowait()

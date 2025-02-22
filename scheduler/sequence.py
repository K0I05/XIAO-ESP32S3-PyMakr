import asyncio

class Sequence:  # Enable asynchronous iterator interface
    
    def __init__(self):
        self._evt = asyncio.Event()
        self._args = None


    def __aiter__(self):
        return self


    async def __anext__(self):
        await self._evt.wait()
        self._evt.clear()
        return self._args


    def trigger(self, args) -> None:
        self._args = args
        self._evt.set()
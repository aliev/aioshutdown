import asyncio
from signal import Signals
from typing import Callable, Coroutine, Any


HandlerType = Callable[[asyncio.AbstractEventLoop, Signals], Coroutine[Any, Any, None]]

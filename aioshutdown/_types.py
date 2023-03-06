import asyncio
from signal import Signals
from typing import Any, Callable, Coroutine

HandlerType = Callable[[asyncio.AbstractEventLoop, Signals], Coroutine[Any, Any, None]]

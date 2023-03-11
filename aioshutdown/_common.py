import asyncio
import sys
from contextlib import AbstractContextManager
from signal import Signals
from typing import Set

from ._shutdown import shutdown
from ._types import HandlerType

if sys.version_info >= (3, 11):  # pragma: nocover
    from typing import Self
else:  # pragma: nocover
    from typing_extensions import Self


class Signal(AbstractContextManager):
    def __init__(self, signal: Signals) -> None:
        self.signal: Signals = signal
        self._signals: Set[Signals] = set()

    def __repr__(self) -> str:
        return repr(self.signal)

    def __str__(self) -> str:
        return str(self.signal)

    def add_signal_handler(
        self,
        handler: HandlerType,
        signal: Signals,
    ) -> None:
        self.loop.add_signal_handler(
            signal, lambda s=signal: asyncio.create_task(handler(self.loop, s))
        )

    def __or__(self, other: Self):
        other._signals.add(self.signal)

        for _signal in self._signals:
            other._signals.add(_signal)

        self._signals.clear()

        return other

    def __enter__(self) -> asyncio.AbstractEventLoop:
        self._signals.add(self.signal)

        self.loop = asyncio.events.new_event_loop()

        for s in self._signals:
            self.add_signal_handler(shutdown, s)

        return self.loop

    def __exit__(self, exc_type, exc_value, traceback):
        self._signals.clear()
        self.loop.close()

import signal

from ._common import Signal

SIGTERM = Signal(signal.SIGTERM)
SIGINT = Signal(signal.SIGINT)
SIGHUP = Signal(signal.SIGHUP)


__all__ = ["SIGTERM", "SIGINT", "SIGHUP", "Signal"]

import asyncio
import logging
import sys
from signal import Signals

logger = logging.getLogger("aioshutdown")


async def shutdown(loop: asyncio.AbstractEventLoop, signal: Signals) -> None:
    """Cleanup tasks tied to the service's shutdown.

    Args:
        loop (asyncio.AbstractEventLoop): Event loop.
        signal (Optional[signal.Signals], optional): OS signal. Defaults to None.
    """
    logger.info("Received exit signal %s...", signal.name)

    # Get the list of all tasks except the current one.
    tasks = [
        t
        for t in asyncio.all_tasks(loop=loop)
        if t is not asyncio.current_task(loop=loop)
    ]

    if sys.version_info >= (3, 9):
        cancel = lambda t: t.cancel(msg=signal)  # noqa: E731
    else:
        cancel = lambda t: t.cancel()  # noqa: E731

    # Request for cancellation of all outstanding tasks.
    for task in tasks:
        cancel(task)

    logger.info("Cancelling %d outstanding tasks", len(tasks))

    # Concurrently wait for all tasks to be cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    logger.info("Stopping event loop")

    loop.stop()

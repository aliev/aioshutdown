import asyncio
import logging
import sys
from signal import Signals

logger = logging.getLogger("aioshutdown")


def cancel(task: asyncio.Task, signal: Signals) -> None:
    if sys.version_info >= (3, 9):  # pragma: nocover
        task.cancel(msg=signal)
    else:  # pragma: nocover
        task.cancel()


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

    # Request for cancellation of all outstanding tasks.
    for task in tasks:
        cancel(task, signal)

    logger.info("Cancelling %d outstanding tasks", len(tasks))

    # Concurrently wait for all tasks to be cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    logger.info("Stopping event loop")

    loop.stop()

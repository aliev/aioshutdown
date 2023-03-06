# aioshutdown

Context manager that provides simple graceful shutdown interface for your asyncio tasks.

## Installation

```
pip install -U aioshutdown
```

## Usage

Just specify the list of signals that you want to intercept using the `|` operator:

```python
from aioshutdown import SIGTERM, SIGINT, SIGHUP


with SIGTERM | SIGHUP | SIGINT as loop:
    ...
```

The context manager will return an instance of the current event loop. You can intercept signals directly inside your coroutines:

```python
async def my_task(sleep: int):
    try:
        """ Main logic of your coroutine. """
    except asyncio.CancelledError as exc:
        """ In this place you can gracefully complete the work. """
```

Full example:


```python
import asyncio
from aioshutdown import SIGTERM, SIGINT, SIGHUP
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

async def my_task(sleep: int):
    try:
        while True:
            logging.info("Sleep from task #%s", sleep)
            await asyncio.sleep(sleep)
    except asyncio.CancelledError as exc:
        # Received an exit signal. In this place we gracefully complete the work.
        signal = exc.args[0] # NOTE: works in Python >= 3.9 only: https://docs.python.org/3/library/asyncio-future.html?highlight=Changed%20in%20version%203.9:%20Added%20the%20msg%20parameter.#asyncio.Future.cancel
        logging.warning("Received %s signal. Shutting down...", signal.value)

# Usage with `run_forever`

with SIGTERM | SIGHUP | SIGINT as loop:
    tasks = [loop.create_task(my_task(i)) for i in range(1, 10)]
    loop.run_forever()

# Usage with `run_until_complete`

with SIGTERM | SIGHUP | SIGINT as loop:
    tasks = [loop.create_task(my_task(i)) for i in range(1, 10)]
    loop.run_until_complete(asyncio.gather(*results))
```

Output

```
23:04:05,798 INFO: Sleep from task #1
23:04:05,798 INFO: Sleep from task #2
23:04:06,799 INFO: Sleep from task #1
23:04:07,800 INFO: Sleep from task #2
23:04:07,800 INFO: Sleep from task #1
23:04:08,801 INFO: Sleep from task #1
^C23:04:09,504 INFO: Received exit signal SIGINT...
23:04:09,504 INFO: Cancelling 2 outstanding tasks
23:04:09,504 WARNING: Received 2 signal. Shutting down...
23:04:09,504 WARNING: Received 2 signal. Shutting down...
23:04:09,504 INFO: Stopping event loop
```


## Useful links

[Graceful Shutdowns with asyncio](https://www.roguelynn.com/words/asyncio-graceful-shutdowns/)

import asyncio
from enum import Enum, auto
from multiprocessing import Pipe, Process, connection

from aioshutdown import SIGHUP, SIGINT, SIGTERM


class TaskStatus(Enum):
    RUNNING = auto()
    STOPPED = auto()


async def task(conn: connection.Connection):
    try:
        while True:
            await asyncio.sleep(1)
            conn.send(TaskStatus.RUNNING)
    except asyncio.CancelledError:
        conn.send(TaskStatus.STOPPED)


def worker(conn: connection.Connection):
    with SIGINT | SIGTERM | SIGHUP as loop:
        loop.create_task(task(conn))
        loop.run_forever()


def test_run_worker():
    conn1, conn2 = Pipe()

    p = Process(target=worker, args=(conn1,))
    p.start()

    counter = 0

    signals = []

    while not conn2.closed:
        status = conn2.recv()
        counter += 1
        if counter == 3:
            p.terminate()

        signals.append(status)

        if status == TaskStatus.STOPPED:
            conn2.close()

    assert TaskStatus.RUNNING in signals
    assert TaskStatus.STOPPED in signals

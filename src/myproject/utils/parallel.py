"""Multiprocessing utilities: producer-consumer and starmap patterns."""

import multiprocessing
from typing import Any, Callable


class Consumer(multiprocessing.Process):
    """Worker process that pulls tasks from a queue and puts results into another."""

    def __init__(
        self,
        task_queue: multiprocessing.JoinableQueue,
        result_queue: multiprocessing.Queue,
    ) -> None:
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self) -> None:
        """Process tasks until a None (poison pill) is received."""
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                self.task_queue.task_done()
                break
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)


def run_producer_consumer(
    tasks: list[Callable[[], Any]],
    num_workers: int | None = None,
) -> list[Any]:
    """Run callables via producer-consumer pattern and collect results.

    Args:
        tasks: List of zero-argument callables to execute.
        num_workers: Number of worker processes (default: 2x CPU count).

    Returns:
        List of results in completion order.
    """
    num_workers = num_workers or multiprocessing.cpu_count() * 2
    task_queue: multiprocessing.JoinableQueue = multiprocessing.JoinableQueue()
    result_queue: multiprocessing.Queue = multiprocessing.Queue()

    consumers = [Consumer(task_queue, result_queue) for _ in range(num_workers)]
    for c in consumers:
        c.start()

    for task in tasks:
        task_queue.put(task)

    # Poison pills
    for _ in range(num_workers):
        task_queue.put(None)

    task_queue.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    return results


def run_starmap(
    func: Callable[..., Any],
    args_list: list[tuple[Any, ...]],
    num_workers: int | None = None,
) -> list[Any]:
    """Run a function across argument tuples using Pool.starmap.

    Args:
        func: Function to call with each set of arguments.
        args_list: List of argument tuples.
        num_workers: Number of worker processes (default: CPU count - 1).

    Returns:
        List of results in input order.
    """
    num_workers = num_workers or max(1, multiprocessing.cpu_count() - 1)
    with multiprocessing.Pool(num_workers) as pool:
        return pool.starmap(func, args_list)

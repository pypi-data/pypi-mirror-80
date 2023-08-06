import asyncio
from concurrent.futures import ALL_COMPLETED, Future, wait
import logging
from threading import Thread
from typing import Any, Coroutine, List, Optional

from aporia.consts import LOGGER_NAME


logger = logging.getLogger(LOGGER_NAME)


class EventLoop:
    """Asyncio event loop manager for worker thread loop."""

    def __init__(self):
        """Initializes an EventLoop instance."""
        logger.debug("Starting event loop in a worker thread.")
        self.loop = asyncio.new_event_loop()
        self.loop_thread = Thread(target=self.run_loop, daemon=True)

        # We keep a list of all tasks that were not awaited, to allow flushing
        # We have to do this manually to support python versions below
        # 3.7 (otherwise we could use asyncio.all_tasks())
        self.futures: List[Future] = []

        self.loop_thread.start()

    def run_loop(self):
        """Runs the asyncio event loop."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_coroutine(self, coro: Coroutine, await_result: Optional[bool] = True) -> Optional[Any]:
        """Runs a coroutine in the worker thread loop.

        Args:
            coro (Coroutine): Coroutine to execute
            await_result (bool, optional): If await_result is True, this will block untill the
                coroutine finishes executing. Defaults to True.

        Returns:
            Optional[Future]: Coroutine return value, if await_result is True
        """
        future = asyncio.run_coroutine_threadsafe(coro=coro, loop=self.loop)

        if await_result:
            return future.result()
        else:
            self.futures.append(future)
            return None

    def flush(self):
        """Waits for all currently scheduled tasks to finish."""
        logger.debug("Waiting for scheduled tasks to finish executing.")
        futures: List[Future] = self.futures
        self.futures = []

        wait(futures, return_when=ALL_COMPLETED)

import asyncio
import itertools
from typing import Any
import httpcore
import httpx

from client.constants import RETRIES_BACKOFF_FACTOR


class AsyncClientWithRetry:
    def __init__(
        self, retries: int = 2, retryExceptions: tuple = (httpcore.ConnectError,)
    ):
        """
        Initialize an async HTTP client with a retry mechanism.

        :param retries: Maximum number of retry attempts
        :param retryExceptions: Exceptions to retry on
        """
        self._retries = retries
        self._retryExceptions = retryExceptions

    def _retry_strategy(self, factor: float):
        """
        Exponential backoff strategy.
        Generate a geometric sequence that has a ratio of 2 and starts with 0.

        For example:
        - `factor = 0.5`: `0s, 0.5s, 1s, 2s, 4s, 8s, 16s, ...`
        - `factor = 2`: `0s, 2s, 4s, 8s, 16s, 32s, 64s, ...`

        :param factor: Current sequence factor
        :return: Seconds to wait before next retry
        """

        yield 0
        for n in itertools.count():
            yield factor * 2**n

    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """
        Send an HTTP request with retry logic.

        :param method: HTTP method (GET, POST, etc.)
        :param url: Request URL
        :param kwargs: Additional httpx.AsyncClient.request arguments
        :return: HTTP response
        """
        retries_left = self._retries
        delays = self._retry_strategy(factor=RETRIES_BACKOFF_FACTOR)

        while True:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.request(method, url, **kwargs)
                    return response
            except self._retryExceptions:
                if retries_left <= 0:
                    raise
                retries_left -= 1
                delay = next(delays)
                await asyncio.sleep(delay)

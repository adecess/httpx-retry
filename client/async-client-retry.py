import httpcore


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

    def _retry_strategy(self):
        pass

    async def request(self):
        pass

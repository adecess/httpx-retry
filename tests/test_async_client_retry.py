from unittest.mock import AsyncMock, patch
import httpcore
import httpx
import pytest

from client.async_client_retry import AsyncClientWithRetry


@pytest.mark.asyncio
async def test_client_third_attempt_successful():
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = [
            httpcore.ConnectError("First connection attempt failed"),
            httpcore.ConnectError("Second connection attempt failed"),
            httpx.Response(
                status_code=200, request=httpx.Request("GET", "http://test.com")
            ),
        ]

        client = AsyncClientWithRetry()

        response = await client.request("GET", "http://test.com")

        assert mock_request.call_count == 3
        assert response.status_code == 200  # 3rd attempt succeeds


@pytest.mark.asyncio
async def test_client_retries_exhausted():
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = httpcore.ConnectError("Connection failed")

        client = AsyncClientWithRetry()

        # Check that httpcore.ConnectError is raised when the request is made
        with pytest.raises(httpcore.ConnectError):
            await client.request("GET", "http://test.com")

        # only 2 retries
        assert mock_request.call_count == 3


@pytest.mark.asyncio
async def test_backoff_retry_strategy():
    with (
        patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep,
        patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request,
    ):
        mock_request.side_effect = [
            httpcore.ConnectError("First attempt failed"),
            httpcore.ConnectError("Second attempt failed"),
            httpx.Response(
                status_code=200, request=httpx.Request("GET", "http://test.com")
            ),
        ]

        client = AsyncClientWithRetry()

        response = await client.request("GET", "http://test.com")

        # Verify backoff times
        assert mock_sleep.call_args_list[0][0][0] == 0  # First attempt delay in seconds
        assert (
            mock_sleep.call_args_list[1][0][0] == 0.5
        )  # Second attempt delay in seconds
        assert response.status_code == 200

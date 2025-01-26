from unittest.mock import AsyncMock, patch
import httpcore
import httpx
import pytest

from client.async_client_retry import AsyncClientWithRetry


@pytest.mark.asyncio
async def test_client_retry_strategy():
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

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_client_retries_exhausted():
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = httpcore.ConnectError("Connection failed")

        client = AsyncClientWithRetry()

        with pytest.raises(httpcore.ConnectError):
            await client.request("GET", "http://test.com")

        assert mock_request.call_count == 3

import asyncio

from client.async_client_retry import AsyncClientWithRetry


async def main():
    client = AsyncClientWithRetry()
    r = await client.request("POST", "https://httpbin.org/post", data={"key": "value"})
    print(r.json())


if __name__ == "__main__":
    asyncio.run(main())

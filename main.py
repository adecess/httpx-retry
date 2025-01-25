import asyncio

from client.async_client_retry import AsyncClientWithRetry


async def main():
    client = AsyncClientWithRetry()
    r = await client.request("GET", "https://www.example.com/")
    print(r)


if __name__ == "__main__":
    asyncio.run(main())

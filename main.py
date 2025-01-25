import httpx
import asyncio


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://www.example.com/")
        print(r)


if __name__ == "__main__":
    asyncio.run(main())

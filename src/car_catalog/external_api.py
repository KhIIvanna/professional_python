import asyncio
import httpx

async def fetch_car_with_retry_and_limit(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    url: str,
    attempts: int = 3,
) -> dict:
    async with semaphore:
        for attempt in range(1, attempts + 1):
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError):
                if attempt == attempts:
                    raise
                await asyncio.sleep(attempt)
        raise RuntimeError("Unexpected retry state")

async def fetch_group_of_cars(base_url: str, car_ids: list[int]) -> list[dict]:
    semaphore = asyncio.Semaphore(3)  # обмеження паралелізму
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [
            asyncio.create_task(
                fetch_car_with_retry_and_limit(
                    client,
                    semaphore,
                    f"{base_url}/cars/{car_id}"
                )
            )
            for car_id in car_ids
        ]
        results = await asyncio.gather(*tasks)
        return list(results)
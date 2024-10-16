import asyncio

import time
import httpx
from bs4 import BeautifulSoup


URL = "https://djinni.co/jobs/"


# ЗАПИТ від  Client:
async def get_djinni_jobs(page: int, client: httpx.AsyncClient, url: str = URL):
    response = await client.get(url, params={"page": page})
    soup = BeautifulSoup(response.content, "html.parser")
    return [job.text.strip() for job in soup.findAll("a", class_="job-item__title-link")]


async def main(start_page: int, stop_page: int) -> None:
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(get_djinni_jobs(page, client, URL))
                for page in range(start_page, stop_page)
            ]
    for task in tasks:
        print(task.result())


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main(1, 20))
    duration = time.perf_counter() - start
    print(duration)

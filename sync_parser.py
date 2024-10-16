import  time
import httpx
from bs4 import BeautifulSoup


URL = "https://djinni.co/jobs/"


# ЗАПИТ від  Client:
def get_djinni_jobs(page: int, client: httpx.Client, url: str = URL):
    response = client.get(url, params={"page": page})
    soup = BeautifulSoup(response.content, "html.parser")
    return [job.text.strip() for job in soup.findAll("a", class_="job-item__title-link")]


def main(start_page: int, stop_page: int) -> None:
    with httpx.Client() as client:
        for page in range(start_page, stop_page):
            print(get_djinni_jobs(page, client, URL))


# ЗАПИТ   БЕЗ Client: (повільніший, тому що є процедура встановлення з'єднання,
# і без клієнта перед кожним запитом вставлюється нове з'єднання)

# def get_djinni_jobs_without_client(page: int, url: str = URL):
#     response = httpx.get(url, params={"page": page})
#     soup = BeautifulSoup(response.content, "html.parser")
#     return [job.text.strip() for job in soup.findAll("a", class_="job-item__title-link")]
#
#
# def main_without_client(start_page: int, stop_page: int) -> None:
#     for page in range(start_page, stop_page):
#         print(get_djinni_jobs_without_client(page, URL))


if __name__ == "__main__":

    start = time.perf_counter()
    main(1, 20)
    duration = time.perf_counter() - start
    print(duration)

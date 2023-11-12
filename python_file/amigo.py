import requests
import random

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import *

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]


class ByUserRequest:
    """
    Класс ByUserRequest используется для извлечения информации с веб-страницы на основе URL-адреса,
    предоставленного пользователем.
    """

    def __init__(self, url):
        self.url = url
        self.items = {}

    def getting(self):
        resp = requests.get(
            self.url, headers={"User-Agent": random.choice(user_agents)}
        )
        soup = BeautifulSoup(resp.content, "lxml")

        self.items["Адрес страницы"] = self.url
        self.items["Раздел"] = (
            soup.find("section", class_="breadcrumbs")
            .text.strip()
            .replace(" \n", "")
            .split(" /")[2]
        )
        self.items["Название"] = soup.find("h1", class_="page-title").text.strip()

        fields = soup.find("dl", class_="ribbon-informer-dl").find_all("dt")
        texts = soup.find("dl", class_="ribbon-informer-dl").find_all("dd")

        for key, value in zip(fields, texts):
            self.items[key.string.strip()] = value.string.strip()

        return self.items


count_go = 271
count_error = []

# Предоставленный блок кода представляет собой цикл while, который выполняет итерацию от count_go
# до тех пор, пока не достигнет 3000.
while count_go < 3000:
    try:
        urlopen(f"https://amigo.ru/search-by-tissues/?ELEMENT_ID={count_go}")
    except HTTPError as e:
        print("HTTP error", e, count_go)
        count_error.append(count_go)
        count_go += 1
    except URLError as e:
        print("Opps ! Page not found!", e, count_go)
        count_error.append(count_go)
        count_go += 1
    else:
        try:
            ByUserRequest(
                f"https://amigo.ru/search-by-tissues/?ELEMENT_ID={count_go}"
            ).getting()
        except Exception as e:
            print("Exception", e, count_go)
            count_error.append(count_go)
            count_go += 1
        else:
            ByUserRequest(
                f"https://amigo.ru/search-by-tissues/?ELEMENT_ID={count_go}"
            ).getting()
            count_go += 1

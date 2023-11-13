import requests
import random
import json

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import *

url = "https://amigo.ru/search-by-tissues/?ELEMENT_ID="

print(
    """
      Сначала введите номер, с которого вы хотите начать
      а затем введите конечный номер.
    """
)
count_start = int(input("start count from = "))
count_end = int(input("end count from = "))

json_result = {"json": []}
count_error = []

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]


def writer():
    with open("data.json", "w", encoding="utf-8") as file:
        file.write(
            json.dumps(
                json_result,
                indent=4,
                ensure_ascii=False,
            )
        )


class ByUserRequest:
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
        self.items["Изображение"] = (
            "https://amigo.ru"
            + soup.find("a", class_="ribbon-informer-slider").attrs["href"]
        )

        fields = soup.find("dl", class_="ribbon-informer-dl").find_all("dt")
        texts = soup.find("dl", class_="ribbon-informer-dl").find_all("dd")

        for key, value in zip(fields, texts):
            self.items[key.string.strip()] = value.string.strip()

        return self.items


while count_start <= count_end:
    try:
        urlopen(url + str(count_start))
    except HTTPError as e:
        print("HTTP error", e, count_start)
        count_error.append(count_start)
        count_start += 1
    except URLError as e:
        print("Opps ! Page not found!", e, count_start)
        count_error.append(count_start)
        count_start += 1
    else:
        try:
            data = ByUserRequest(url + str(count_start)).getting()
        except Exception as e:
            print("Exception", e, count_start)
            count_error.append(count_start)
            count_start += 1
        else:
            print("Start import data to file", count_start)
            json_result["json"].append(data)
            count_start += 1

if count_start == count_end + 1:
    with open("error.json", "w", encoding="utf-8") as file:
        print("Write final data to file")
        print("Write error data to file")
        writer()
        file.write(json.dumps(count_error))

# print(ByUserRequest("https://amigo.ru/search-by-tissues/?ELEMENT_ID=271").getting())

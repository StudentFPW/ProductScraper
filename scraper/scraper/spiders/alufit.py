import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AlufitSpider(CrawlSpider):
    name = "alufit"
    allowed_domains = ["alufit.ru"]
    start_urls = ["https://alufit.ru/katalog"]

    rules = (
        Rule(
            LinkExtractor(allow=r"gotovyie-izdeliya"),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        table = response.css("div.af-introtext.af-cell-half-width").get().strip()
        return {"url": response.url, "data": table}


# import re
# pattern = re.compile("<.*?>")
# if table is not None:
#     item["table"] = (
#         re.sub(
#             pattern,
#             "",
#             response.css("div.af-introtext.af-cell-half-width").get(),
#         )
#         .replace("\n", " > ")
#         .replace("\r", "")
#     )
# return {"table": item.get("table"), "url": response.url}

# item["Адрес страницы: "] = response.url
# item["Название: "] = ""
# item["Цена, руб: "] = ""
# item["Ширина: "] = ""
# item["Высота: "] = ""
# item["Тип жалюзи: "] = ""
# item["Цвет: "] = ""
# item["Ширина ламели (см): "] = ""
# item["Материал: "] = ""
# item["Прозрачность: "] = ""
# item["Открытие: "] = ""
# item["Крепление: "] = ""
# item["Автоматика: "] = ""
# item["Раздел: "] = ""

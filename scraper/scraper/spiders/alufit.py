import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AlufitSpider(CrawlSpider):
    name = "alufit"
    allowed_domains = ["alufit.ru"]
    start_urls = ["https://alufit.ru"]

    rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        item = {}
        item["Адрес страницы: "] = response.url
        item["Название: "] = ""
        item["Цена, руб: "] = ""
        item["Ширина: "] = ""
        item["Высота: "] = ""
        item["Тип жалюзи: "] = ""
        item["Цвет: "] = ""
        item["Ширина ламели (см): "] = ""
        item["Материал: "] = ""
        item["Прозрачность: "] = ""
        item["Открытие: "] = ""
        item["Крепление: "] = ""
        item["Автоматика: "] = ""
        item["Раздел: "] = ""
        return item

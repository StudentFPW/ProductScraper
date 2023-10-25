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
        # response.css("table.table-product").getall() TABLE
        # response.css("td.bb::text")[8].get().strip() FIELD
        # response.css("td.nobb b::text")[8].get().strip() TEXT

        item = {}
        fields = response.css("td.bb::text").getall()
        texts = response.css("td.nobb b::text").getall()

        name = response.css("div.af-h1.af-h1-ha h1::text").get()
        price = response.css("span.af-product-price__value span::text").get()
        position = response.css("li.breadcrumb-item span::text")[2].get()

        for key, value in zip(fields, texts):
            if name or price or position is not None:
                item["Название"] = name.strip()
                item["Цена, руб"] = (
                    price.strip() + " " + response.css("span.ruble::text").get().strip()
                )
                item["Раздел"] = position.strip()
            item[key.strip()] = value.strip()

        return {"Адрес страницы": response.url, "Данные": item}


# item["Адрес страницы: "] = ""
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

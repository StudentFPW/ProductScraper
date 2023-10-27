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
        item = {}

        fields = response.css("td.bb::text").getall()
        texts = response.css("td.nobb b::text").getall()

        item["Адрес страницы:"] = response.url
        name = response.css("div.af-h1.af-h1-ha h1::text").get()
        price = response.css("span.af-product-price__value span::text").get()
        position = " ".join(
            response.css("li.breadcrumb-item span::text")[-1].get().split()[0:2]
        )

        for key, value in zip(fields, texts):
            if name or price or position is not None:
                item["Название:"] = name.strip()
                item["Цена, руб:"] = (
                    price.strip() + " " + response.css("span.ruble::text").get().strip()
                )
                item["Раздел:"] = position.strip()
            item[key.strip()] = value.strip().replace(", ", " | ").replace("/", " | ")
        return item


# search_string= "Горизонтальные жалюзи 0221 Белый глянцевый 55х160 см"
# word="Горизонтальные жалюзи"
# lword=len(word)
# start_index=search_string.find(word)
# extracted_string= search_string[start_index:start_index+lword]
# print(extracted_string)

# response.css("table.table-product").getall() TABLE
# response.css("td.bb::text")[8].get().strip() FIELD
# response.css("td.nobb b::text")[8].get().strip() TEXT

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

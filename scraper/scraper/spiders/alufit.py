import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# https://alufit.ru/katalog/shtoryi-zebra/ TODO URL OF MAIN PAGE MENU

# https://msk.alufit.ru/katalog/rolonnyie-shtoryi/na-ramu-okna/minirulonnyie-shtoryi/ TODO URL OF PRODUCT


class AlufitSpider(CrawlSpider):
    name = "alufit"
    allowed_domains = ["alufit.ru"]
    start_urls = ["https://alufit.ru"]

    rules = (
        # Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True), TODO DEFAULT
        Rule(
            LinkExtractor(
                allow=("katalog",),
                deny=(
                    "czenyi",
                    "nashi-rabotyi",
                    "kontaktyi",
                    "o-kompanii",
                    "skidki",
                    "oplata",
                    "podobrat-reshenie",
                    "uslugi",
                    "sotrudnichestvo",
                    "vopros-otvet-faq",
                    "politika-konfidenczialnosti",
                    "garantiya-i-vozvrat",
                ),
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        item = {}
        item["Адрес страницы"] = (response.url,)
        item["Название"] = (response.css("ul.breadcrumb span::text")[-1].get().strip(),)
        item["Цена"] = (
            response.css("span.af-product-price__value span::text")[1].get().strip(),
        )
        item["Ширина по умолчанию"] = (
            response.css("input.input-plus-minus::attr(value)")[0].get().strip(),
        )
        item["Высота по умолчанию"] = (
            response.css("input.input-plus-minus::attr(value)")[1].get().strip(),
        )
        item["Тип жалюзи"] = (
            response.css("ul.breadcrumb span::text")[-1].get().strip(),
        )
        item["Цвет по умолчанию"] = (
            response.css("span.color-caption::text")[0].get().strip(),
        )
        item["Прозрачность по умолчанию"] = (
            response.css("input.bmd-ripple::attr(value)")[0].get().strip(),
        )
        item["Управление по умолчанию"] = (
            response.css("span.radio-label::text")[0].get().strip(),
        )
        item["Тип установки по умолчанию"] = (
            response.css("span.radio-label::text")[5].get().strip(),
        )
        item["Раздел"] = response.css("ul.breadcrumb span::text")[2].get().strip()
        return item

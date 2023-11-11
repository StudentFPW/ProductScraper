from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# https://amigo.ru/dealer/informatsiya-o-nalichii/nal_rul/
# https://amigo.ru/search-by-tissues/?ELEMENT_ID=2847


class AmigoSpider(CrawlSpider):
    name = "amigo"
    allowed_domains = ["amigo.ru"]
    start_urls = ["https://amigo.ru"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    # "nal_rul",
                    # "nal_zebra",
                    # "nal_plisse",
                    # "nal_vert",
                    # "nal_vert_plast",
                    # "nal_vert_al",
                )
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        item = {}

        fields = response.css("dl.ribbon-informer-dl dt::text").getall()
        texts = response.css("dl.ribbon-informer-dl dd::text").getall()

        item["Адрес страницы"] = response.url
        item["Название"] = response.css("h1.page-title::text").get().strip()
        item["Раздел"] = " / ".join(response.css("div.cont span::text")[1:8:2].getall())

        for key, value in zip(fields, texts):
            item[key.strip()] = value.strip().replace(", ", " | ").replace("/", " | ")

        return item

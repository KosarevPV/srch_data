import scrapy
from scrapy.http import HtmlResponse


class DzenRuSpider(scrapy.Spider):
    name = "dzen_ru"
    allowed_domains = ["dzen.ru"]
    start_urls = ["https://dzen.ru/news/?issue_tld=ru&utm_referer=gb.ru"]
    # //h2/a
    def parse(self, response: HtmlResponse):
        pass

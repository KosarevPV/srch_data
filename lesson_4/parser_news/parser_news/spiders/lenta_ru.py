from datetime import date

import scrapy
from scrapy.http import HtmlResponse

from lesson_4.parser_news.parser_news.items import ParserNewsItem


class LentaRuSpider(scrapy.Spider):
    name = "lenta_ru"
    allowed_domains = ["lenta.ru"]
    start_urls = ["http://lenta.ru/"]

    def parse(self, response: HtmlResponse):
        news = response.xpath("//div/a")
        for i in news[3:-9]:
            source = self.allowed_domains[0]
            text = i.xpath('.//text()').get()
            href = i.xpath('./@href').get()
            news_date = str(date.today())

            yield ParserNewsItem(
                source=source,
                text=text,
                href=href,
                news_date=news_date,
            )

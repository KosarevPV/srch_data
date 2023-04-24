# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserNewsItem(scrapy.Item):
    _id = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()
    href = scrapy.Field()
    news_date = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    name = scrapy.Field()
    employer = scrapy.Field()
    location = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    href = scrapy.Field()


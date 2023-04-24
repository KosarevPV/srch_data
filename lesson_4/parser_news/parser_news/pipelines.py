# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ParserNewsPipeline:
    def __init__(self):
        client = MongoClient()
        self.mongo_db = client.parser_news

    def process_item(self, item, spider):
        collection = self.mongo_db.lenta
        collection.insert_one(item)
        return item

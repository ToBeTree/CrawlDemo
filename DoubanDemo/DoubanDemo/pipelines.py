# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo


class DoubandemoPipeline(object):
    def process_item(self, item, spider):
        return item


class DoubanMoviePipeline(object):
    COLLECTION_NAME = 'douban_movie'

    def __init__(self, mongo_url, mongo_port, mongo_db):
        self.seen = set()  # 用于item去重
        self.mongo_url = mongo_url
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
        )

    def process_item(self, item, spider):
        if spider.name == 'douban_movie':
            if item['imdd'] in self.seen:
                raise DropItem(item)
            self.seen.add(item['imdd'])
            self.database[self.COLLECTION_NAME].insert(dict(item))
        return item

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url, self.mongo_port)
        self.database = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

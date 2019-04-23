# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class CorpspiderPipeline(object):
    collection_name = 'corps'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'corps')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, list):
          for i in item:
            self.process_item(item, spider)
          return
        if item['tp'] == 'corp':
            old = self.db[self.collection_name].find_one({ "no": item['no'] })
            if old:
              print 'update corp...'
              self.db[self.collection_name].update_one({'_id': old['_id'] }, {'$set': dict(item)})
            else:
              print 'insert corp....'
              self.db[self.collection_name].insert(dict(item))
        if item['tp'] == 'qualification':
            old = self.db['qualifications'].find_one({ "no": item['no'], "name": item["name"] })
            if old:
              self.db['qualifications'].update_one({'_id': old['_id'] }, {'$set': dict(item)})
            else:
              self.db['qualifications'].insert(dict(item))
        return item

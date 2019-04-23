# -*- coding: utf-8 -*-
import scrapy
import time
import re
from ..mongo import db
from ..items import CorpspiderItem

class ChachaSpider(scrapy.Spider):
    name = 'tianyan'
    # allowed_domains = ['www.qichacha.com']
    start_urls = [
        'https://www.tianyancha.com'
    ]
    items = []
    skip = 0

    def get_item(self):
        if len(self.items) <= 0:
            for item in db['corps'].find({ 'email': None }).skip(self.skip).limit(10):
                self.items.append(item)
            self.skip += 10
        self.items.pop()

    def start_requests(self):
        item = self.get_item()
        url = 'https://www.tianyancha.com/search?key=' + item['no']
        yield scrapy.Request(url, callback=self.parseSearch, meta={ 'no': item['no'], 'name': item['name'], '_id': item['_id'] })

    def parse(self, response):
        print "parse......"
        amount = response.xpath('//td[@width="308px"]/div/@title').extract_first()
        item = CorpspiderItem()
        corp_id = response.meta['_id']
        item['register_amount'] = amount.strip()
        db['corps'].update_one({'_id': corp_id }, {'$set': dict(item)})

        titles = response.xpath('//div[@class="detail "]/div/span[@class="link-hover-click"]/text()').extract()
        for title in titles:
            print title
        # item['created_at'] = 
        # return item



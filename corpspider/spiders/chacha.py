# -*- coding: utf-8 -*-
import scrapy
import time
import re
from ..mongo import db
from ..items import CorpspiderItem
import random
import sys

reload(sys)

class ChachaSpider(scrapy.Spider):
    name = 'chacha'
    allowed_domains = ['www.qichacha.com']
    start_urls = [
        'https://www.qichacha.com'
    ]
    items = []
    skip = 0

    def get_item(self):
        if len(self.items) <= 0:
            for item in db['corps'].find({ 'email': None }).skip(self.skip).limit(10):
                self.items.append(item)
            self.skip += 10
        if len(self.items) > 0:
            return self.items.pop()
        elif self.skip == 0:
            return None
        else:
            self.skip = 0
            return self.get_item()

    def start_requests(self):
        item = self.get_item()
        while item:
            yield self.request_page(item)
            rd = random.randint(3, 20)
            print 'sleep.... %s' % rd
            time.sleep(rd)
            item = self.get_item()
    def request_page(self, corp):
        url = 'https://www.qichacha.com/search?key=' + corp['no']
        return scrapy.Request(
            url,
            callback=self.parse,
            meta={ 'no': corp['no'], 'name': corp['name'], '_id': corp['_id'] },
            headers={'Referer': 'https://www.baidu.com/'}
        )

    def parse(self, response):
        print "parse......"
        corp_id = response.meta['_id']
        item = CorpspiderItem()

        titles = response.xpath('//span[@class="m-l"]/text()').extract()
        for title in titles:
            if(title.find(u'注册资本：') >= 0):
                item['register_amount'] = re.findall(u'注册资本：(.*)', title)[0]
            elif(title.find(u'成立时间：') >= 0):
                item['created_at'] = re.findall(u'成立时间：(.*)', title)[0]
            elif(title.find(u'电话：') >= 0):
                item['phone'] = re.findall(u'电话：(.*)', title)[0]
            else:
                print 'not found' + title
        titles = response.xpath('//p[@class="m-t-xs"]/text()').extract()
        email = None
        for title in titles:
            if(title.find(u'邮箱：') >= 0):
                email = re.findall(u'邮箱：(.*)', title)[0]
                item['email'] = email
            else:
                print 'not found' + title
        if not email:
            print response.body
        item['no'] = response.meta['no']
        print(dict(item))
        db['corps'].update_one({'_id': corp_id }, {'$set': dict(item)})



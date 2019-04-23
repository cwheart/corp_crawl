# -*- coding: utf-8 -*-
import scrapy
import time
import re
from ..mongo import db
from ..items import CorpspiderItem
import random

class ChachaSpider(scrapy.Spider):
    name = 'chacha'
    # allowed_domains = ['www.qichacha.com']
    start_urls = [
        'https://www.qichacha.com/search?key=91110000625906144E'
    ]
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

    def start_requests(self):
        count = db['corps'].count({})
        skip = 0
        step = 10
        url = ''
        while skip < count:
            items = db['corps'].find({ 'email': None }).limit(step).skip(skip)
            skip += step
            for item in items:
                rd = random.randint(3, 20)
                print "sleep... %s" % rd
                time.sleep(rd)
                url = 'https://www.qichacha.com/search?key=' + item['no']
                print url
                yield scrapy.Request(url, callback=self.parse, headers={ 'Referer': 'https://www.baidu.com/' })
    def parseSearch(self, response):
        url = response.xpath('//div[@id="content_left"]/div[@id="1"]/div/a[@class="m"]/@href').extract_first()
        if url:
            yield scrapy.Request(url, callback=self.parse)
        else:
            print 'skip...'
    def parse(self, response):
        print "parse......"
        item = CorpspiderItem()
        item['tp'] = 'corp'
        no = response.xpath('//em/text()').extract_first()
        item['no'] = no.strip()

        titles = response.xpath('//span[@class="m-l"]/text()').extract()
        for title in titles:
            if(title.find(u'注册资本：') >= 0):
                item['register_amount'] = re.findall(u'注册资本：(.*)', title)[0]
            if(title.find(u'成立时间：') >= 0):
                item['created_at'] = re.findall(u'成立时间：(.*)', title)[0]
            if(title.find(u'电话：') >= 0):
                item['phone'] = re.findall(u'电话：(.*)', title)[0]
        titles = response.xpath('//p[@class="m-t-xs"]/text()').extract()
        for title in titles:
            if(title.find(u'邮箱：') >= 0):
                item['email'] = re.findall(u'邮箱：(.*)', title)[0]
        return item

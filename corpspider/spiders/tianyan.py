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
        'https://www.qichacha.com/search?key=91110000625906144E'
    ]
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'

    def start_requests(self):
        count = count = 20 # db['corps'].find({}).count()
        skip = 0
        step = 10
        while skip < count:
            items = db['corps'].find({ 'email': None }).limit(step).skip(skip)
            skip += step
            for item in items:
                url = 'https://www.baidu.com/s?wd=site%3Atianyancha.com%20' + item['no'] + '%20' + item['name'] + u'_工商信息'
                yield scrapy.Request(url, callback=self.parseSearch, headers={ "USER_AGENT": self.agent })
                time.sleep(4)
    def parseSearch(self, response):
        links = response.xpath('//div[@class="result c-container "]')
        i = 0
        for link in links:
            i += 1
            text = link.xpath('.//h3/a/em/text()').extract_first()
            url = link.xpath('.//h3/a/@href').extract_first() # 链接页面
            # url = link.xpath('.//div[@class="f13"]//a[@class="m"]/@href').extract_first() # 百度快照页面
            if text and text.find(u"_工商信息") >= 0:
                yield scrapy.Request(url, callback=self.parse, headers={ "USER_AGENT": self.agent })
                return
            else:
                print 'skip...'
        print 'not found...'
    def parse(self, response):
        print "parse......"
        amount = response.xpath('//td[@width="308px"]/div/@title').extract_first()
        item = CorpspiderItem()
        item['tp'] = 'corp'
        item['register_amount'] = amount.strip()

        titles = response.xpath('//table[@class="table -striped-col -border-top-none -breakall"]/tbody/tr/td/text()').extract()
        item['no'] = titles[7]

        titles = response.xpath('//div[@class="detail "]/div/span[@class="link-hover-click"]/text()').extract()
        for title in titles:
            print title
        # item['created_at'] = 
        # return item



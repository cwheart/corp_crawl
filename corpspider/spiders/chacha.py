# -*- coding: utf-8 -*-
import scrapy
import time
from ..mongo import db

class ChachaSpider(scrapy.Spider):
    name = 'chacha'
    # allowed_domains = ['www.qichacha.com']
    start_urls = [
        'https://www.qichacha.com/search?key=91110000625906144E'
        'https://www.qichacha.com/search?key=91110000625906144E'
        'https://www.qichacha.com/search?key=91110000625906144E'
        'https://www.qichacha.com/search?key=91110000625906144E'
        'https://www.qichacha.com/search?key=91110000625906144E'
        'https://www.qichacha.com/search?key=91110000625906144E'
    ]
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'

    def start_requests(self):
        count = db['corps'].find({}).count()
        skip = 0
        step = 10
        while skip < count:
            items = db['corps'].find({}).limit(step).skip(skip)
            skip += step
            for item in items:
                time.sleep(20)
                url = 'https://www.qichacha.com/search?key=' + item['no']
                yield scrapy.Request(url, callback=self.parse, headers={ "USER_AGENT": self.agent })
    def parse(self, response):
        print response.body

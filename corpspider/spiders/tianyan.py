# -*- coding: utf-8 -*-
import scrapy
import time
import re
from ..mongo import db
from ..items import CorpspiderItem
import random
from ..holder import Holder, HolderItem

class ChachaSpider(scrapy.Spider):
    name = 'tianyan'
    allowed_domains = ['www.tianyancha.com']
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
        return self.items.pop()

    def start_requests(self):
        yield self.request_list()
    def request_list(self):
        corp = self.get_item()
        url = 'https://www.tianyancha.com/search?key=' + corp['no']
        return scrapy.Request(
            url,
            callback=self.parse_list,
            dont_filter=True,
            meta={ 'no': corp['no'], 'name': corp['name'], '_id': corp['_id'] }
        )
    def parse_list(self, response):
        no = response.meta['no']
        corp_id = response.meta['_id']
        url = response.xpath('//a[@class="name select-none"]/@href').extract_first()
        if url:
            time.sleep(1)
            yield self.request_page(url, no, corp_id)
        else:
            print 'there is no link' + no
        rd = random.randint(3, 15)
        print 'sleep.... %s' % rd
        time.sleep(rd)
        yield self.request_list()

    def request_page(self, url, no, corp_id):
        print "url....."
        print url
        return scrapy.Request(
            url,
            callback=self.parse,
            meta={ 'no': no, '_id': corp_id }
        )

    def parse(self, response):
        print "parse......"
        corp_id = response.meta['_id']
        no = response.meta['no']


        # 股东信息
        holder = Holder.objects(corp_id=corp_id)

        hoder_count = response.xpath('//div[@id="nav-main-holderCount"]/span[@class="data-count"]/text()').extract_first()
        lines = response.xpath('//div[@id="_container_holder"]/table/tbody/tr')
        items = []
        for line in lines:
            arr = line.xpath('.//td/div/span/text()').extract()
            amount = arr[0]
            paid_at = arr[1]
            percent = line.xpath('.//td/div/div/span[@class=""]/text()').extract_first()
            name = line.xpath('.//td/div/div[@class="dagudong"]/a/text()').extract_first()
            extra = line.xpath('.//td/div/span/a/text()').extract_first()
            tags = line.xpath('.//td/div[@class="dagudong"]/span/text()').extract()
            if not tags:
                tags = []
            item = HolderItem(corp_no=no, amount=amount, percent=percent, name=name, paid_at=paid_at,extra=extra,tags=tags)
            items.append(item)
            
        holder.modify(
            upsert=True,
            new=True,
            set__items=items,
            set__corp_no=no,
            set__hoder_count=hoder_count
        )
        print hoder_count
        # holder.save()



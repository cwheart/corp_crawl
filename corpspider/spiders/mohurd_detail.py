# -*- coding: utf-8 -*-
import scrapy
import time
import random
from ..mongo import db

class MohurdDetailSpider(scrapy.Spider):
    name = 'mohurd_detail'
    allowed_domains = ['jzsc.mohurd.gov.cn']
    start_urls = [
        'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list'
    ]

    items = []
    skip = 0

    def get_item(self):
        if len(self.items) <= 0:
            for item in db['corps'].find({ 'legal_person': None, 'link': {'$ne': None } }).skip(self.skip).limit(10):
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
            time.sleep(4)
            yield self.request_qualification(item)
            time.sleep(4)
            item = self.get_item()
    
    def request_page(self, corp):
        url = corp['link']
        return scrapy.Request(
            url,
            callback=self.parse,
            meta={ 'no': corp['no'], 'name': corp['name'], '_id': corp['_id'], 'link': url }
        )
    
    def request_qualification(self, corp):
        corp_id = corp['link'].split('/')[-1]
        url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/" + corp_id
        return scrapy.Request(
            url,
            callback=self.pase_qualification,
            meta={ 'no': corp['no'], 'name': corp['name'], '_id': corp['_id'], 'link': corp['link'] }
        )

    def parse(self, response):
        print "parse......"
        link = response.meta['link']
        items = response.xpath('//table[@class="pro_table_box datas_table"]/tbody/tr/td/text()').extract()
        item = {}
        item['no'] = items[0].strip().split('/')[-1].strip()
        item['legal_person'] = items[1].strip()
        item['corp_type'] = items[2].strip()
        item['area'] = items[3].strip()
        item['address'] = items[4].strip()
        db['corps'].update({ 'link': link }, {'$set': dict(item) })

    def pase_qualification(self, response):
        print "parse......"
        corp_id = response.meta['_id']
        link = response.meta['link']
        corp = db['corps'].find({ 'link': link })[0]
        corp_no = corp['no']
        lines = response.xpath('//tr[@class="row"]')
        for line in lines:
            items = line.xpath('.//td/text()').extract()
            qua_type = items[1].strip()
            no = items[2].strip()
            name = items[3].strip()
            published_at = items[4].strip()
            expired_at = items[5].strip()
            published_org = items[6].strip()
            item = {}
            item['qua_type'] = qua_type
            item['no'] = no
            item['name'] = name
            item['published_at'] = published_at
            item['expired_at'] = expired_at
            item['published_org'] = published_org
            old = db['qualifications'].find_one({ "no": item['no'], "name": item["name"] })
            if old:
              self.db['qualifications'].update_one({'_id': old['_id'] }, {'$set': dict(item)})
            else:
              self.db['qualifications'].insert(dict(item))




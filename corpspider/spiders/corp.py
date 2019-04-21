# -*- coding: utf-8 -*-
import scrapy
import re
import time
from ..items import CorpspiderItem

class CorpSpider(scrapy.Spider):
    name = 'corp'
    # allowed_domains = ['jzsc.mohurd.gov.cn']
    start_urls = ['http://jzsc.mohurd.gov.cn/dataservice/query/comp/list']

    def start_requests(self):
        yield self.request_page('1')

    def request_page(self, page):
        url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list'
        request = scrapy.FormRequest(
            url = url,
            formdata = {"apt_code" : "D101A", "apt_scope" : "建筑工程施工总承包一级", "$reload": "0", "$total": "7299", "$pgsz": "15", "$pg": page},
            callback = self.parse
        )
        return request

    def parse(self, response):
        urls = response.xpath('//td[@class="text-left primary"]/a/@href').extract()
        for path in urls:
            url = response.urljoin(path)
            time.sleep(8)
            yield scrapy.Request(url, callback=self.parse_detail)
        page_text = response.css('a[sf=pagebar]').attrib['sf:data']
        page = re.findall(r'\(\{pg\:(\d+)', page_text)[0]
        page = int(page) + 1
        yield self.request_page("%s" % page)

    def parse_detail(self, response):
        items = response.xpath('//table[@class="pro_table_box datas_table"]/tbody/tr/td/text()').extract()
        item = CorpspiderItem()
        item['name'] = response.xpath('//div[@class="user_info spmtop"]/b/text()').extract_first()
        item['no'] = items[0]
        item['legal_person'] = items[1]
        item['corp_type'] = items[2]
        item['area'] = items[3]
        item['address'] = items[4]
        print item
        return item

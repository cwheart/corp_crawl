# -*- coding: utf-8 -*-
import scrapy
import re

class CorpSpider(scrapy.Spider):
    name = 'corp'
    allowed_domains = ['http://jzsc.mohurd.gov.cn']
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
    def request_detail(self, path):
        return scrapy.Request("http://jzsc.mohurd.gov.cn" + path, callback = self.parse_detail)

    def parse(self, response):
        urls = response.xpath('//table[@class="table_box responsive personal"]/tbody/tr/td[@class="text-left primary"]/a/@href').extract()
        for path in urls:
            print path
            yield self.request_detail(path)

    def parse_detail(self, response):
        titles = response.xpath('//table[@class="pro_table_box datas_table"]/tbody/tr/td/text()')
        for title in titles:
            print title

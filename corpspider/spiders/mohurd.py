# -*- coding: utf-8 -*-
import scrapy
import re
import time
from ..items import CorpspiderItem
from ..items import QualificationItem
from ..mongo import db

class MohurdSpider(scrapy.Spider):
    name = 'mohurd'
    # allowed_domains = ['jzsc.mohurd.gov.cn']
    start_urls = ['http://jzsc.mohurd.gov.cn/dataservice/query/comp/list']
    url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list'
    i = 0
    j = 0
    total = ""
    apt_codes = [
        'D101A',
        'D101T',
        'D110A',
        'D110T'
    ]
    apt_scopes = [
        '建筑工程施工总承包一级',
        '建筑工程施工总承包特级',
        '市政公用工程施工总承包一级',
        '市政公用工程施工总承包特级'
    ]
    codes = [
        '110000',
        '120000',
        '130000',
        '140000',
        '150000',
        '210000',
        '220000',
        '230000',
        '310000',
        '320000',
        '330000',
        '340000',
        '350000',
        '360000',
        '370000',
        '410000',
        '420000',
        '430000',
        '440000',
        '450000',
        '460000',
        '500000',
        '510000',
        '520000',
        '530000',
        '540000',
        '610000',
        '620000',
        '630000',
        '640000',
        '650000'
    ]
    areas = [
        '北京市',
        '天津市',
        '河北省',
        '山西省',
        '内蒙古自治区',
        '辽宁省',
        '吉林省',
        '黑龙江省',
        '上海市',
        '江苏省',
        '浙江省',
        '安徽省',
        '福建省',
        '江西省',
        '山东省',
        '河南省',
        '湖北省',
        '湖南省',
        '广东省',
        '广西壮族自治区',
        '海南省',
        '重庆市',
        '四川省',
        '贵州省',
        '云南省',
        '西藏自治区',
        '陕西省',
        '甘肃省',
        '青海省',
        '宁夏回族自治区',
        '新疆维吾尔自治区'
    ]

    def start_requests(self):
        yield self.request_page('1', 0, 0)

    def request_page(self, page, i, j):
        area = self.areas[i]
        code = self.codes[i]
        apt_scope = self.apt_scopes[j]
        apt_code = self.apt_codes[j]
        print "area: " + code + " scope: " + apt_code + " page: " + page

        request = scrapy.FormRequest(
            url = self.url,
            formdata={
                "apt_code": apt_code,
                "apt_scope": apt_scope,
                "qy_reg_addr": area,
                "qy_region": code,
                "$reload": "0",
                "$total": self.total,
                "$pgsz": "15",
                "$pg": page
            },
            callback=self.parse,
            meta={'i': i, 'j': j}
        )
        return request

    def parse(self, response):
        lines = response.xpath('//tbody[@class="cursorDefault"]/tr')
        for line in lines:
            path = line.xpath('.//td[@class="text-left primary"]/a/@href').extract_first()
            no = line.xpath('.//td[@class="text-left complist-num"]/text()').extract_first()
            if no:
                no = no.strip()
            else:
                continue
            corp_id = path.split("/")[-1]
            # count = db['corps'].count({'no': no.strip()})
            # if count > 0:
            #     time.sleep(1)
            #     continue

            url = response.urljoin(path)
            time.sleep(10)
            yield scrapy.Request(url, callback=self.parse_detail)
            time.sleep(2)
            qualification_url = "http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/" + corp_id
            print qualification_url
            yield scrapy.Request(qualification_url, callback=self.parse_qualification, meta={ 'no': no })
        page_text = response.css('a[sf=pagebar]').attrib['sf:data']
        pg = re.findall(r'\(\{pg\:(\d+)', page_text)[0]
        pc = re.findall(r'pc\:(\d+)', page_text)[0]
        self.total = re.findall(r'tt\:(\d+)', page_text)[0]
        pg = int(pg) + 1
        pc = int(pc)
        print page_text
        i = response.meta['i']
        j = response.meta['j']
        if pg > pc or pg > 30:
            j += 1
            pg = 1
            self.total = ""
        if j >= len(self.apt_scopes):
            i += 1
            j = 0
        print "current" + " i: %s" % i + " j: %s" % j
        yield self.request_page("%s" % pg, i, j)

    def parse_detail(self, response):
        items = response.xpath('//table[@class="pro_table_box datas_table"]/tbody/tr/td/text()').extract()
        item = CorpspiderItem()
        item['tp'] = 'corp'
        item['name'] = response.xpath('//div[@class="user_info spmtop"]/b/text()').extract_first().strip()
        item['no'] = items[0].strip().split('/')[-1].strip()
        item['legal_person'] = items[1].strip()
        item['corp_type'] = items[2].strip()
        item['area'] = items[3].strip()
        item['address'] = items[4].strip()
        return item

    def parse_qualification(self, response):
        result = []
        no = response.meta['no']
        lines = response.xpath('//tr[@class="row"]')
        for line in lines:
            item = QualificationItem()
            item['tp'] = 'qualification'
            item['corp_no'] = no
            items = line.xpath('.//td/text()').extract()
            item['qua_type'] = items[1].strip()
            item['no'] = items[2].strip()
            item['name'] = items[3].strip()
            item['published_at'] = items[4].strip()
            item['expired_at'] = items[5].strip()
            item['published_org'] = items[6].strip()
            result.append(item)
        return result

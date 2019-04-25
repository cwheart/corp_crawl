# -*- coding: utf-8 -*-
import scrapy
import re
import time
from ..items import CorpspiderItem
from ..items import QualificationItem
from ..mongo import db
from ..corp import Corp

class MohurdSpider(scrapy.Spider):
    name = 'mohurd_link'
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
        i = response.meta['i']
        j = response.meta['j']
        lines = response.xpath('//tbody[@class="cursorDefault"]/tr')
        for line in lines:
            path = line.xpath('.//td[@class="text-left primary"]/a/@href').extract_first()
            url = response.urljoin(path)
            no = line.xpath('.//td[@class="text-left complist-num"]/text()').extract_first()
            corp_name = line.xpath('.//td[@class="text-left primary"]/a/text()').extract_first()
            if no:
                no = no.strip()
                if no == '':
                    continue
                corp_name = corp_name.strip()
            else:
                continue
            corps = Corp.objects(no=no, name=corp_name)
            if len(corps) > 0:
                corp = corps[0]
            else:
                corp = Corp(no=no, name=corp_name)
            corp['link'] = url
            if j == 0:
                corp['d101a']=True
            elif j == 1:
                corp['d101t']=True
            elif j == 2:
                corp['d110a']=True
            elif j == 3:
                corp['d110t']=True
            corp.save()
        page_text = response.css('a[sf=pagebar]').attrib['sf:data']
        pg = re.findall(r'\(\{pg\:(\d+)', page_text)[0]
        pc = re.findall(r'pc\:(\d+)', page_text)[0]
        self.total = re.findall(r'tt\:(\d+)', page_text)[0]
        pg = int(pg) + 1
        pc = int(pc)
        print page_text
        if pg > pc or pg > 30:
            j += 1
            pg = 1
            self.total = ""
        if j >= len(self.apt_scopes):
            i += 1
            j = 0
        print "current" + " i: %s" % i + " j: %s" % j
        time.sleep(4)
        yield self.request_page("%s" % pg, i, j)

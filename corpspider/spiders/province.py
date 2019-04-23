# -*- coding: utf-8 -*-
import scrapy
import re
import time
from ..items import ProvinceItem
from ..mongo import db

class ProvinceSpider(scrapy.Spider):
    name = 'province'
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
        yield self.request_page()

    def request_page(self):
        area = self.areas[self.i]
        code = self.codes[self.i]
        apt_scope = self.apt_scopes[self.j]
        apt_code = self.apt_codes[self.j]
        print area + " " + apt_scope + " " + code

        request = scrapy.FormRequest(
            url = self.url,
            formdata = {
                "apt_code": apt_code,
                "apt_scope": apt_scope,
                "qy_reg_addr": area,
                "qy_region": code,
                "$reload": "0",
                "$pgsz": "15"
            },
            callback = self.parse,
            meta={ 'area': area, 'apt_scope': apt_scope, 'code': code }
        )
        return request

    def parse(self, response):
        page_text = response.css('a[sf=pagebar]').attrib['sf:data']
        total = re.findall(r'tt\:(\d+)', page_text)[0]
        item = ProvinceItem()
        item['tp'] = 'province'
        item['apt_scope'] = response.meta['apt_scope']
        item['area'] = response.meta['area']
        item['code'] = response.meta['code']
        item['total'] = total
        old = db['provinces'].find_one({ "code": item['code'], "apt_scope": item["apt_scope"] })
        if old:
          db['provinces'].update_one({'_id': old['_id'] }, {'$set': dict(item)})
        else:
          db['provinces'].insert(dict(item))
        self.j += 1
        if self.j >= len(self.apt_scopes):
            self.j = 0
            self.i += 1
        time.sleep(10)
        yield self.request_page()
       

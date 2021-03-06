# -*- coding: utf-8 -*-
import scrapy
import re
import time
from ..items import CorpspiderItem
from ..items import QualificationItem
from ..mongo import db
from ..corp import Corp

class MohurdSpider(scrapy.Spider):
    name = 'mohurd2'
    url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list'
    apt_scopes = [
        ['D101A', '建筑工程施工总承包一级'],
        ['D101T', '建筑工程施工总承包特级'],
        ['D110A', '市政公用工程施工总承包一级'],
        ['D110T', '市政公用工程施工总承包特级']
    ]
    areas = [
        ['110000', '北京市'],
        ['120000', '天津市'],
        ['130000', '河北省'],
        ['140000', '山西省'],
        ['150000', '内蒙古自治区'],
        ['210000', '辽宁省'],
        ['220000', '吉林省'],
        ['230000', '黑龙江省'],
        ['310000', '上海市'],
        ['320000', '江苏省'],
        ['330000', '浙江省'],
        ['340000', '安徽省'],
        ['350000', '福建省'],
        ['360000', '江西省'],
        ['370000', '山东省'],
        ['410000', '河南省'],
        ['420000', '湖北省'],
        ['430000', '湖南省'],
        ['440000', '广东省'],
        ['450000', '广西壮族自治区'],
        ['460000', '海南省'],
        ['500000', '重庆市'],
        ['510000', '四川省'],
        ['520000', '贵州省'],
        ['530000', '云南省'],
        ['540000', '西藏自治区'],
        ['610000', '陕西省'],
        ['620000', '甘肃省'],
        ['630000', '青海省'],
        ['640000', '宁夏回族自治区'],
        ['650000', '新疆维吾尔自治区']
    ]

    def start_requests(self):
        for area in areas:
            for scope in apt_scopes:
                yield self.request_page('1', area, scope)


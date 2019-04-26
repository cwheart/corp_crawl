# -*- coding: utf-8 -*-
import scrapy
import re
import time
from ..items import CorpspiderItem
from ..items import QualificationItem
from ..mongo import db
from ..corp import Corp
import sys
from urllib import quote, urlencode
from urllib import urlencode

reload(sys)

sys.setdefaultencoding('utf8')

class FirstNameSpider(scrapy.Spider):
    name = 'first_name'
    url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list'
    i = 0
    j = 0
    total = ''
    lines = open("/data/xc.csv", "r").readlines()
    names = ' '.join(lines).split(' ')

    apt_scopes = [
        ['D101A', '建筑工程施工总承包一级'],
    ]
    areas = [
        ['320000', '江苏省'],
        ['330000', '浙江省'],
        ['420000', '湖北省'],
        ['510000', '四川省'],
    ]

    def start_requests(self):
        yield self.request_page('1', 0, 0)

    def request_page(self, page, i, j):
        code = self.areas[i][0]
        area = self.areas[i][1]
        name = self.names[j]
        apt_code = self.apt_scopes[0][0]
        apt_scope = self.apt_scopes[0][1]
        print "area: " + code + " name: " + name + " page: " + page + " scope: " + apt_code

        request = scrapy.FormRequest(
            url = self.url,
            formdata={
                "apt_code": apt_code,
                "apt_scope": apt_scope,
                "qy_reg_addr": area,
                "qy_fr_name": name,
                "qy_region": code,
                "$reload": "0",
                "$total": self.total,
                "$pgsz": "15",
                "$pg": page
            },
            callback=self.parse,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
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
            if url == 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list':
                print "blank...."
                print i
                print j
                continue
            no = line.xpath('.//td[@class="text-left complist-num"]/text()').extract_first()
            corp_name = line.xpath('.//td[@class="text-left primary"]/a/text()').extract_first()
            if not no:
                no = ''
            if not corp_name:
                print 'corp name blank.. ' + url
                continue
            no = no.strip()
            corp_name = corp_name.strip()
            corps = Corp.objects(no=no, name=corp_name)
            if len(corps) > 0:
                print 'update corp..' + url
                corp = corps[0]
            else:
                print 'new corp.. ' + url
                corp = Corp(no=no, name=corp_name)
            corp['link'] = url
            corp['d101a']=True
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
        if j >= len(self.names):
            i += 1
            j = 0
        print "current" + " i: %s" % i + " j: %s" % j
        time.sleep(4)
        yield self.request_page("%s" % pg, i, j)

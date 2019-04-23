# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CorpspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tp = scrapy.Field() # 数据类型
    no = scrapy.Field()
    name = scrapy.Field()
    legal_person = scrapy.Field()
    corp_type = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    register_amount = scrapy.Field()
    created_at = scrapy.Field()
    pass

class QualificationItem(scrapy.Item):
    tp = scrapy.Field() # 数据类型
    corp_no = scrapy.Field()
    no = scrapy.Field() # 证书编号
    name = scrapy.Field() # 证书名称
    qua_type = scrapy.Field() # 资质类别
    published_at = scrapy.Field() # 发证日期
    expired_at = scrapy.Field() # 证书有效期
    published_org = scrapy.Field() # 发证机关
    pass

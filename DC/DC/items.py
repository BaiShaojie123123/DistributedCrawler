# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DcItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    pass
class JingDongDaoJia(scrapy.Item):
    # define the fields for your item here like:
    skuid = scrapy.Field()
    name = scrapy.Field()
    Class = scrapy.Field()
    price = scrapy.Field()
    imgsrc = scrapy.Field()
    goods_id = scrapy.Field()
    sourceType = scrapy.Field()
class jdDetail(scrapy.Item):
    # define the fields for your item here like:
    source_id = scrapy.Field()
    goods_id = scrapy.Field()
    source_type = scrapy.Field()
    weight = scrapy.Field()
    imgArr = scrapy.Field()
    pass
class jdComment(scrapy.Item):
    # define the fields for your item here like:
    source_id = scrapy.Field()
    goods_id = scrapy.Field()
    source_type = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()
    # 展示的添加时间
    add_time = scrapy.Field()
    pass
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
    pass
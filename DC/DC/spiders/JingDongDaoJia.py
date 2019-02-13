# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from ..items import *
import redis
import pymysql

class JDDJ(scrapy.spiders.Spider):
    #获取skuid的爬虫
    name = "JDDJ_url"

    def __init__(self):

        self.item = JingDongDaoJia()
        self.page = {
            'Fruit': 192,
            'Fish': 260,
            'Meat': 179,
            'Frozen_snacks':171,
            'Vegetable':259
        }
        self.url = {
            'Fruit': 'https://list.jd.com/list.html?cat=12218,12221&page=',
            'Fish': 'https://list.jd.com/list.html?cat=12218,12222&page=',
            'Meat': 'https://list.jd.com/list.html?cat=12218,13581&page=',
            'Frozen_snacks': 'https://list.jd.com/list.html?cat=12218,13591&page=',
            'Vegetable': 'https://list.jd.com/list.html?cat=12218,13553&page='
        }

    def start_requests(self):
        for Key,Value in self.url.items():
            for i in range(self.page[Key]):
                url = Value + str(i+1)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        productList = Selector(text=response.body).xpath('//li[contains(@class, "gl-item")]').extract()
        Class = Selector(text=response.body).xpath('//div[contains(@class, "s-title")]/h3').css('b::text').extract()[0]
        print(Class)
        for item in productList:
            name = Selector(text=item).xpath('//div[contains(@class, "p-name")]/a').css('em::text').extract()[0].strip()
            skuid = Selector(text=item).xpath('//div[contains(@class, "p-operate")]/a[1]/@data-sku').extract()[0]

            self.item['name'] = name
            self.item['skuid'] = skuid
            self.item['Class'] = Class
            yield self.item






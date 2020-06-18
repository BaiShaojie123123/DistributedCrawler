# -*- coding: utf-8 -*-
import os
import re
import time
from random import random
import scrapy
from scrapy.selector import Selector
from .. import filterStr
from .. import settings
from ..DB import DB
from ..items import JingDongDaoJia
import redis
import pymysql
from ..settings import SOURCE_TYPE_JD
from ..user import UserModel



class JDDJ(scrapy.spiders.Spider):
    # 获取skuid的爬虫
    name = "JDDJ_url"

    def __init__(self):

        # 搜索词
        searchKeyWord = '海之蓝'
        # 线上分类id
        self.catId = '641'
        # 想获取多少条数据
        self.getNum = 10
        self.num = 0
        self.supplier_id = 0

        self.item = JingDongDaoJia()
        self.page = {
            'Fruit': 1,
        }
        self.url = {
            'Fruit': 'https://search.jd.com/Search?keyword='+searchKeyWord+'&qrst=1&stock=1&click=0&page=',
        }

    def start_requests(self):
        for Key, Value in self.url.items():
            for i in range(self.page[Key]):
                url = Value+ str(i + 1)
                time.sleep(1)
                yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

    def parse(self, response):

        productList = Selector(text=response.body).xpath('//li[contains(@class, "gl-item")]').extract()

        # $object = UPLOAD_PATH.$new_path.md5(time().mt_rand(100, 999999999)).
        # '.'.pathinfo($file->getInfo('name'), PATHINFO_EXTENSION);
        # $new_path = 'goods'.date('Y').'/'.date('m-d').'/';

        Class = Selector(text=response.body).xpath('//div[contains(@class, "p-name p-name-type-2")]//em[not(i)]').extract()
        print(Class)

        for item in productList:
            if self.num>self.getNum:
                break
            name = Selector(text=item).xpath('//div[contains(@class, "p-name")]/a/em').extract()[0]
            name = filterStr.filter_tags(name)
            skuid = Selector(text=item).xpath('//li/@data-sku').extract()[0]
            price= Selector(text=item).xpath('//div[contains(@class, "p-price")]/strong/i').extract()[0]
            price = filterStr.filter_tags(price)
            imgsrc = Selector(text=item).xpath('//li[contains(@class, "gl-item")]//img/@src').extract()[0]
            imgsrc = imgsrc.replace('//','')



            # 去除京东超市
            # '京东超市金龙鱼 食用油 葵花籽清香型 食用植物调和油5L（新老包装随机发货）'
            name = name.replace("京东超市", "")
            name = name.replace("（京东定制）", "")
            name = name.replace("（京东定制装）", "")
            name = name.replace("京东自营", "")
            name = name.replace("（新老包装随机发货）", "")
            name = name.replace("新旧包装随机配送", "")
            name = name.replace("新老包装随机发放", "")
            name = name.replace("（新老包装随机发放，数量有限，赠完为止）", "")
            name = name.replace("中粮出品", "")
            name = name.replace("（中粮出品）", "")
            if "【沃尔玛】" in name:
                continue
            name = name.replace("【沃尔玛】", "")
            self.item['name'] = name.strip()
            self.item['price'] = price
            self.item['skuid'] = skuid
            # self.item['Class'] = Class
            self.item['imgsrc'] = imgsrc
            self.item['sourceType'] = SOURCE_TYPE_JD
            self.item['goods_id'] = self.insertGoods(self.item)
            self.num = self.num+1

            yield self.item


    def insertGoods(self,data):
            tp_goods_spider = DB('tp_goods_spider')
            skuid = data['skuid']
            goods_id = tp_goods_spider.field('goods_id').where(
                [['source_id', '=', skuid], ['source_type', '=', 1]]).order('goods_id desc').limit('1').fieldOne()
            info = {
                'source_id': data['skuid'],

                'market_price': data['price'],
                'source_type': SOURCE_TYPE_JD,
                'cat_id':self.catId,
                'supplier_id':self.supplier_id,
            }

            # 不存在商品则写入
            if not goods_id:

                info['create_time'] = time.time()
                # 创建时才有名称 更新时不需要spiderUp
                info['goods_name'] = data['name']
                # 增加
                DB('tp_goods_spider').insert(info)
                goods_id = DB('tp_goods_spider').getLastId()

                print('增加商品' + str(goods_id))
            else:
                DB('tp_goods_spider').where([['goods_id','=',goods_id]]).update(info)
                print('更新商品' + str(goods_id))
                info['update_time'] = time.time()
            return goods_id

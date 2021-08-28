# -*- coding: utf-8 -*-
import json
import math
import os
import re
import time
import urllib
import random

import scrapy
from scrapy.selector import Selector

from .. import filterStr, dirMk
from .. import settings
from ..DB import DB
from ..items import JingDongDaoJia, jdDetail
import redis
import pymysql

from ..settings import SOURCE_TYPE_JD, spider_status_type_image
from ..user import UserModel
import numpy as np

class JDDJ(scrapy.spiders.Spider):
    # 获取skuid的爬虫
    name = "JDDJ_Detail"

    def __init__(self):
        self.item = jdDetail()
        self.lastId = DB('spider_status').field('word_value').where([['type', '=', spider_status_type_image],['keyword','=','goods_id']]).limit('1').fieldOne()
        # self.lastId = '0'
        self.maxId = 0
        if self.lastId:
            self.lastId=self.lastId

    def start_requests(self):

        offset = 0
        limit = 1
        count = 0
        TF = True
        while TF:
            condition = [['source_type','=',SOURCE_TYPE_JD],['goods_id','>',str(self.lastId)]]
            if self.maxId > 0:
                condition.append(['goods_id','<',str(self.maxId)])
            kuidList = DB('tp_goods_spider').where(condition).limit(str(limit)).findAll()
            if len(kuidList)==0:
                break
            for goods_item in kuidList:
                time.sleep(0.5)
                source_id = goods_item['source_id']
                goods_id = goods_item['goods_id']
                url ='https://item.jd.com/'+str(source_id)+'.html'
                self.lastId = goods_item['goods_id']
                DB('spider_status').where([['type','=',spider_status_type_image],['keyword','=','goods_id']]).update({'word_value':str(self.lastId)})
                yield scrapy.Request(url=url, callback=self.parse,meta={'goods_id':goods_id,'source_id':source_id,},dont_filter=True)

    def parse(self, response):
        goods_id = response.meta['goods_id']
        source_id = response.meta['source_id']
        vv = random.randint(1,10)
        str_J_ = ''
        skuid = str(source_id)
        str_J_ = str_J_ + 'J_' + skuid + '%2C'
        # str2 = str2 + skuid + '%2C'
        # str_AD_ = str_AD_ + 'AD_' + skuid + '%2C'
        # 价格
        # urlPrice = 'https://p.3.cn/prices/mgets?callback=jQuery' + self.getParam() + '&ext=11100000pdtk=&pduid=' + str(random.randint(100000, 999999)) + '&pdpin=&pin=null&type=1&area=1_72_55653_0&source=item-pc&skuIds=' + str_J_
        # listPrice = self.getPrice(urlPrice)

        goods_weight =  Selector(text=response.body).xpath("//div[@class='p-parameter']/ul[@class='parameter2 p-parameter-list']/li").extract()
        weight = ''
        for weightitem in goods_weight:
            weight = filterStr.filter_tags(weightitem)
            if '商品毛重' not in weight:
                continue
            weight = weight.replace('商品毛重：','')
            weight = weight.replace('kg','')
            break


        imgArr =  Selector(text=response.body).xpath('//div[contains(@class, "spec-items")]//img/@src').extract()


        #图片地址 jfs/t1 替换为  s546x546_jfs/t1
        self.item['weight'] = weight
        self.item['imgArr'] = imgArr
        self.item['source_id'] = source_id
        self.item['goods_id'] = goods_id
        self.item['source_type'] = SOURCE_TYPE_JD

        self.insertGoods(self.item)

        yield self.item
    def insertGoods(self,data):






        tp_goods_spider = DB('tp_goods_spider')
        goods_id = data['goods_id']
        goods_find_id = tp_goods_spider.field('goods_id').where(
            [['goods_id', '=', goods_id], ['source_type', '=', 1]]).order('goods_id desc').limit('1').findOne()
        info = {
            'weight': data['weight'],
            # 'goods_name': data['name'],
            # 'market_price': data['price'],
            # 'source_type': SOURCE_TYPE_JD
        }
        # 不存在商品则写入
        if  goods_find_id:
            DB('tp_goods_spider').where([['goods_id','=',goods_id]]).update(info)
            print('更新商品' + str(goods_id))
        return goods_id
    def getParam(self):
        return str(math.floor(10000000*np.random.rand(1)))
    def getPrice(self,url):
        print(url)
        list = []
        try:
            pattern = re.compile('\[.*]')
            # url = 'https://p.3.cn/prices/mgets?callback=jQuery5548626&type=1&area=1_72_55653_0&pdtk=&pduid=1531278026&pdpin=&pin=null&pdbp=0&skuIds=J_5436612%2CJ_3378602%2CJ_6356269%2CJ_3165584%2CJ_100004807065%2CJ_100001286654&ext=11100000&source=item-pc'
            response = urllib.request.urlopen(url)
            response = response.read()
            m = pattern.search(str(response))
            value = json.loads(m.group())
            data1 = json.dumps(value,ensure_ascii=False)
            data2 = json.loads(data1)
            for item in data2:
                dict = {}
                price = item['p']
                dict['price'] = price
                try:
                    plus_p = item['tpp']
                    dict['plus_p'] = plus_p
                except:
                    dict['plus_p'] = '无'
                list.append(dict)
        except:
            print('请求频繁,再次尝试中')
            time.sleep(1)
            list = self.getPrice(url)
        return list
    def getBaseData(self,url):
        print(url)
        list = []
        try:
            pattern = re.compile('\[.*]')
            # url = 'https://p.3.cn/prices/mgets?callback=jQuery5548626&type=1&area=1_72_55653_0&pdtk=&pduid=1531278026&pdpin=&pin=null&pdbp=0&skuIds=J_5436612%2CJ_3378602%2CJ_6356269%2CJ_3165584%2CJ_100004807065%2CJ_100001286654&ext=11100000&source=item-pc'
            response = urllib.request.urlopen(url)
            response = response.read()
            m = pattern.search(str(response))
            value = json.loads(m.group())
            data1 = json.dumps(value,ensure_ascii=False)
            data2 = json.loads(data1)
            for item in data2:
                dict = {}
                price = item['p']
                dict['price'] = price
                try:
                    plus_p = item['tpp']
                    dict['plus_p'] = plus_p
                except:
                    dict['plus_p'] = '无'
                list.append(dict)
        except:
            print('请求频繁,再次尝试中')
            time.sleep(1)
            list = self.getPrice(url)
        return list




        # 获取配送数据
        # #获取cat
        # catUrl = Selector(text=response.body).xpath("//div[@class='inner border']/div[@class='head']/a/@href").extract()[0]
        # catUrl = urllib.parse.urlparse(catUrl)
        # query = catUrl.query
        # query = urllib.parse.parse_qsl(query)
        # cat = ''
        # for p in query:
        #     if 'cat' == p[0]:
        #         cat = p[1]
        #         break
        #
        # venderId = Selector(text=response.body).xpath("//div[@class='follow J-follow-shop']/@data-vid").extract()[0]
        # # https://c0.3.cn/stock?skuId=12295984164&area=1_72_55653_0&venderId=659016&cat=1320,1584,2676&pduid=460134
        # # https://c0.3.cn/stock?skuId=7210120&area=1_72_55653_0&venderId=1000014142&cat=1320,1584,13790&pduid=1531278026
        # # https://c0.3.cn/stock?skuId=4360445&area=1_72_55653_0&venderId=1000040105&buyNum=1&choseSuitSkuIds=&cat=1320,1584,2675&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=1531278026&ch=1&callback=jQuery9379361
        #
        # baseDataUrl = 'https://c0.3.cn/stock?skuId='+skuid+'&area=1_72_55653_0&buyNum=1&venderId='+venderId+'&cat='+cat+'&fqsp=0&pdpin=&&pduid='+ str(random.randint(1000000000, 9999999999))+'&ch=1&callback=jQuery'+str(random.randint(1000000, 9999999))
        # listPrice = self.getBaseData(baseDataUrl)
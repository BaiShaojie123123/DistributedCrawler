# -*- coding: utf-8 -*-
import datetime
import json
import math
import os
import re
import time
import urllib
import random
from urllib import request

import chardet
import scrapy
from scrapy.selector import Selector

from .. import filterStr, dirMk
from .. import settings
from ..DB import DB
from ..items import JingDongDaoJia, jdDetail, jdComment
import redis
import pymysql

from ..settings import SOURCE_TYPE_JD, BASE_PATH
from ..strHelp import calc_md5
from ..user import UserModel
import numpy as np

class JDDJ(scrapy.spiders.Spider):
    # 获取skuid的爬虫
    name = "JDDJ_Comment"

    def __init__(self):

        self.spider_status_type = '2'
        self.item = jdComment()
        self.lastId = DB('spider_status').field('word_value').where([['type', '=', self.spider_status_type],['keyword','=','goods_id']]).limit('1').fieldOne()
        # self.lastId = '0'
        self.maxId = 0
        if self.lastId:
            self.lastId=self.lastId

        self.page = {
            'commentPage': 20,
        }
        self.url = {
            'commentPage': 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&score=0&sortType=5&pageSize=10&isShadowSku=0&rid=0&fold=1&productId=',
        }

    def start_requests(self):

        offset = 0
        limit = 50
        count = 0
        TF = True
        while TF:
            time.sleep(0.5)
            condition = [['source_type','=',SOURCE_TYPE_JD],['goods_id','>',str(self.lastId)],['prod_goods_id','<>','0'],['is_on_sale','=','1']]
            if self.maxId > 0:
                condition.append(['goods_id','<',str(self.maxId)])
            kuidList = DB('tp_goods_spider').where(condition).limit(str(limit)).findAll()
            if len(kuidList)==0:
                break
            for goods_item in kuidList:
                for Key, Value in self.url.items():
                    for i in range(self.page[Key]):
                        url=''
                        time.sleep(0.5)
                        source_id = goods_item['source_id']
                        goods_id = goods_item['goods_id']
                        url = Value+str(source_id)+'&page='+str(i + 1)
                        self.lastId = goods_item['goods_id']
                        DB('spider_status').where([['type','=',self.spider_status_type],['keyword','=','goods_id']]).update({'word_value':str(self.lastId)})
                        yield scrapy.Request(url=url, callback=self.parse,meta={'goods_id':goods_id,'source_id':source_id,},dont_filter=True)

    def parse(self, response):
        goods_id = response.meta['goods_id']
        source_id = response.meta['source_id']
        ret = chardet.detect(response.body)
        encoding = ret['encoding']
        if not encoding:
            return
        responseStr = str(response.body, encoding = encoding)

        cc = responseStr.find('({')
        if cc<0:
            return
        cc = int(cc+1)
        lastIndex = int(responseStr.rfind('}'))
        responseStr = responseStr[cc:lastIndex+1]
        responseArr = json.loads(responseStr)

        comments = responseArr['comments']

        for item in comments:
            #图片地址 jfs/t1 替换为  s546x546_jfs/t1
            item['content'] = item['content'].replace('京东','阿鲤家配齐')

            self.item['content'] = item['content']
            self.item['source_id'] = item['id']
            self.item['goods_id'] = goods_id
            images = ''
            if 'images' in item.keys():
                images = item['images']
            add_time = item['creationTime']
            date_time =datetime.datetime.strptime(add_time,"%Y-%m-%d %H:%M:%S")
            add_time = time.mktime(date_time.timetuple())
            self.item['add_time'] = int(add_time)
            self.item['images'] = images
            self.item['source_type'] = SOURCE_TYPE_JD

            self.insertGoods(self.item)

            yield self.item
    def insertGoods(self,data):

        tp_goods_spider = DB('tp_comment_spider')
        tp_comment_images_spider = DB('tp_comment_images_spider')
        source_id = data['source_id']
        goods_id = data['goods_id']
        goods_find_id = tp_goods_spider.field('comment_id').where(
            [['source_id', '=', source_id], ['source_type', '=', 1],['goods_id','=',goods_id]]).order('source_id desc').limit('1').findOne()
        info = {
            'source_id': data['source_id'],
            'source_type': SOURCE_TYPE_JD,
            'goods_id' : goods_id,
        }
        # 不存在商品则写入
        if not goods_find_id:
            info['add_time']= data['add_time']
            info['content']= data['content']
            info['create_time'] = time.time()
            # 匿名评价
            info['is_anonymous']= str(1)
            info['zan_num'] = str(random.randint(0, 30))
            info['deliver_rank'] = str(random.randint(3, 5))
            info['goods_rank'] = str(random.randint(3, 5))
            info['service_rank'] = str(random.randint(3, 5))
            info['is_show'] = '1'
            if data['images']:
                info['img'] = 1
            # 增加
            dd = DB('tp_comment_spider')
            inser = dd.insert(info)
            comment_id = dd.getLastId()
            print('增加评论' + str(comment_id))
        else:
            comment_id = goods_find_id['comment_id']

        # 如果有评论图片
        if data['images']:
            for image in data['images']:

                imgsrc = image['imgUrl']
                imgsrc= imgsrc.replace('//','')
                imgsrc= imgsrc.replace('n0/s128x96_jfs/','shaidan/s616x405_jfs/')
                all_path = dirMk.get_all_path(imgsrc,'public/upload/comment')
                imgsrc = 'http://'+imgsrc
                search_image_url = calc_md5(imgsrc)
                comment_image_find_id = tp_comment_images_spider.field('comment_id').where(
                    [['comment_id', '=', comment_id], ['image_url_md5', '=', search_image_url],['goods_id','=',goods_id]]).limit('1').findOne()
                if not comment_image_find_id:
                    insertPath = all_path.replace(BASE_PATH, '')
                    down = request.urlretrieve(imgsrc,all_path)
                    if down:
                        image_insert = {
                            'image_url':insertPath,
                            'image_url_md5':search_image_url,
                            'source_url':imgsrc,
                            'goods_id':str(goods_id),
                            'comment_id' : str(comment_id),

                        }
                        tp_comment_images_spider.insert(image_insert)
                        # 图片不存在则下载并写入数据库
        return comment_id

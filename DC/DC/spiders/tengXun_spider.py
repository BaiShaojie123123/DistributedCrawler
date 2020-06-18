# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from ..items import *
import redis
import pymysql

class tc_Spider(scrapy.spiders.Spider):
    name = "tcSpider"

    def __init__(self):
        self.pattern = re.compile(r'https://new.qq.com/.*')
        self.item = DcItem()
        self.r = redis.Redis(host='127.0.0.1', port=6379,db=2)
        self.hostUrl = 'https://new.qq.com/'
        self.db = pymysql.connect('localhost','root','3.141592653579','chineseword',charset='utf8' )

    def start_requests(self):
        '''
        如果待爬队列为空那么需要启动两次爬虫程序，第一次爬取hostirl的内容,第二次爬取队列内容,并填充队列
        :return:
        '''
        if self.r.llen('tcSpider:items') == 0:
            yield scrapy.Request(url=self.hostUrl, callback=self.parse)
        while self.r.llen('tcSpider:items')> 0:
            url = eval(self.r.lpop('tcSpider:items'))['url']
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #获取<a>的href值
        urlList = Selector(text=response.body).css('a').xpath('@href').extract()
        #获取中文
        chinese = self.getChinese(response.body.decode('utf-8'))
        #插入mysql
        self.InsertMysql(chinese)
        for url in urlList:
            if self.pattern.search(url):
                self.item['url'] = url
                yield self.item

    def getChinese(self,str):
        pattern = "[\u4e00-\u9fa5]+"
        regex = re.compile(pattern)
        results = regex.findall(str)
        str = ''
        for r in results:
            str = str+r
        return str
    def InsertMysql(self,str):
        cursor = self.db.cursor()
        sql = "INSERT INTO table1(word) VALUES ('%s')" % (str)
        try:
            cursor.execute(sql)
            self.db.commit()
            print('--------------------------------------------------------------')
        except:
            self.db.rollback()
            print('**************************************************************')

    def CloseMysql(self):
        self.db.close()




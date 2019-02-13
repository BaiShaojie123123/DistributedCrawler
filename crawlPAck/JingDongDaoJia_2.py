# -*- coding: utf-8 -*-
import re
import random
import math
import redis
import urllib
import openpyxl
from openpyxl.workbook import Workbook
import numpy as np
import json
import time

class JingDongDaoJia_2():

    def __init__(self):

        self.r = redis.Redis(host='127.0.0.1', port=6379,db=2)
        self.outwb = Workbook()
        self.wo = self.outwb.active

    def start_requests(self):
        i = 0
        size = 60
        TF = True
        careerSheet = self.getCareerSheet()
        while TF:  #有数据时标记为true
            urlList = self.r.lrange("JDDJ_url:items", i*size, (i+1)*60)
            str_J_ = ''
            str2 = ''
            str_AD_ = ''
            if len(urlList) > 0:  #取到数据不跳出，取不到数据跳出。
                i = i + 1
                for item in urlList:
                    #name = eval(item)['name']
                    #Class = eval(item)['Class']
                    skuid = eval(item)['skuid']
                    str_J_ = str_J_+'J_'+skuid+'%2C'
                    str2 = str2 + skuid + '%2C'
                    str_AD_ = str_AD_ + 'AD_' + skuid + '%2C'
                time.sleep(1)
                urlPrice = 'https://p.3.cn/prices/mgets?callback=jQuery' + self.getParam() + '&ext=11101000&pin=&type=1&area=1_72_2799_0&skuIds='+str_J_
                urlChatCount = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds='+str2+'&callback=jQuery'+self.getParam()+'&_=1548229360349'
                url_AD= 'https://ad.3.cn/ads/mgets?&callback=jQuery'+self.getParam()+'&my=list_adWords&source=JDList&skuids='+str_AD_

                listPrice = self.getPrice(urlPrice)
                listChatCount = self.getChatCount(urlChatCount)
                list_AD = self.getAD(url_AD)

                for index in range(len(urlList)):
                    try:
                        careerSheet.append([
                                            eval(urlList[index])['skuid'],
                                            eval(urlList[index])['name'],
                                            eval(urlList[index])['Class'],
                                            listPrice[index]['price'],
                                            listPrice[index]['plus_p'],
                                            listChatCount[index]['GoodCount'],
                                            listChatCount[index]['GeneralCount'],
                                            listChatCount[index]['PoorCount'],
                                            str(listChatCount[index]['GoodRateShow'])+'%',
                                            list_AD[index]['ad']
                        ])
                    except:
                        print('数据不足')
                print('第' + str(i * 60) + '条爬取成功')
            else:
                print('超出数据库范围')
                TF = False

    def getParam(self):
        return str(math.floor(10000000*np.random.rand(1)))

    def getPrice(self,url):
        print(url)
        list = []
        try:
            pattern = re.compile('\[.*]')
            response = urllib.request.urlopen(url)
            m = pattern.search(str(response.read()))
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

    def getChatCount(self,url):
        print(url)
        list = []
        try:
            pattern = re.compile('\[.*]')
            response = urllib.request.urlopen(url)
            m = pattern.search(str(response.read().decode('GBK')))
            value = json.loads(m.group())
            data1 = json.dumps(value)
            data2 = json.loads(data1)
            for item in data2:
                dict = {}
                try:
                    dict['GoodCount'] = item['GoodCount'] #好评
                except:
                    dict['GoodCount'] = '无'  # 好评
                try:
                    dict['GeneralCount'] = item['GeneralCount']  # 中评
                except:
                    dict['GeneralCount'] = '无'
                try:
                    dict['PoorCount'] = item['PoorCount']  # 差评
                except:
                    dict['PoorCount'] = '无'
                try:
                    dict['GoodRateShow'] = item['GoodRateShow']  # 分数
                except:
                    dict['GoodRateShow'] = '无'
                list.append(dict)
        except:
            print('请求频繁，再次尝试中')
            time.sleep(1)
            list = self.getChatCount(url)
        return list

    def getAD(self,url):
        print(url)
        list = []
        try:
            pattern = re.compile('\[.*]')
            response = urllib.request.urlopen(url)
            m = pattern.search(str(response.read().decode('utf-8')))
            value = json.loads(m.group())
            data1 = json.dumps(value,ensure_ascii=False)
            data2 = json.loads(data1)

            for item in data2:
                dict = {}
                dict['ad'] = item['ad']
                list.append(dict)
        except:
            print('请求频繁,再次尝试中')
            time.sleep(1)
            list = self.getAD(url)
        return list

    def getCareerSheet(self):
        careerSheet = self.outwb.create_sheet('all', 0)
        careerSheet.append(['skuid', '名称','品类', '售卖价', '会员价', '好评数', '中评数', '差评数', '好评%','特色标语'])
        return careerSheet

    def SaveExcel(self):
        self.outwb.save("E:\DataAnalysis\\tools\python3\project\DistributedCrawler\JDDJ.xlsx")

if __name__ == '__main__':
    jddj = JingDongDaoJia_2()
    jddj.start_requests()
    jddj.SaveExcel()
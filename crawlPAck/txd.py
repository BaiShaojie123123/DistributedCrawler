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

import request


class txd():

    def __init__(self):

        self.r = redis.Redis(host='127.0.0.1', port=6379,db=2)
        self.outwb = Workbook()
        self.wo = self.outwb.active

    def start_requests(self):

        data ={"shopIds":"288146005","catId":"txd_10017653","catIds":"[{\"backendCatId\":\"127530071,127530073\",\"catId\":\"txd_10017653\",\"categoryType\":\"3\",\"displayProperties\":\"0\",\"enableNisitc\":\"0\",\"enableOrder\":\"0\",\"extend\":{\"hasInventoryItemCount\":\"26\",\"noInventoryItemCount\":\"0\",\"hasInventoryItemCountStrategy\":\"GICfBE\",\"noInventoryItemCountStrategy\":\"GICfBE\"},\"firstCatId\":\"txd_10017249\",\"isIgraph\":\"0\",\"itemCount\":\"26\",\"noInventoryItemCount\":\"0\",\"parentCatId\":\"txd_10017274\",\"ruleIds\":[],\"ruleWeight\":\"0\",\"tags\":\"\",\"title\":\"家常叶菜\",\"totalItemCount\":\"26\",\"type\":\"0\"}]","pagination":"-1-51-1-0","busiType":"classify","order":"","needProperties":0}
        params = {
            'jsv': '2.5.0',
            'appKey': 12574478,
            't': int(time.time()*1000),
            'sign': 'dccded4f1e98f36940da3f6a723fbe46',
            'v': 1.0,
            'dataType': 'jsonp',
            'timeout': 10000,
            'api': 'mtop.wdk.classify.txdqueryclassifypage',
            'jsonpIncPrefix': 'weexcb',
            'ttid': '2020@weex_h5_1.0.36',
            'type': 'jsonp',
            'callback': 'mtopjsonpweexcb6',
            'data': str(data)
        }
        response = request.get(url='https://h5api.m.taobao.com/h5/mtop.wdk.classify.txdqueryclassifypage/1.0/',params=params)
        a  =1

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
        self.outwb.save("/Users/baishaojie/python/jdgithub/JDDJ.xlsx")

jddj = txd()
jddj.start_requests()
jddj.SaveExcel()
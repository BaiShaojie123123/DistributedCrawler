from scrapy.http import Request
import requests
import redis
import urllib
import re
'''
r = redis.Redis(host='127.0.0.1', port=6379,db=2)
urlList = r.lrange("JDDJ_url:items", 57111, 57112)
# url = eval(r.lpop('JDDJ:items'))['name']
if len(urlList) >0:
    for item in urlList:
        print(eval(item)['name'])
        print(eval(item)['skuid'])
else:
    print('超出数据库范围')
'''
import sys
from Setting.IpFilter import IpFilter
import time
import json
import random

'''
from selenium import webdriver
chromeOptions = webdriver.ChromeOptions() # 设置代理
chromeOptions.add_argument("--proxy-server=HTTP://119.101.112.145:9999") # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(chrome_options = chromeOptions) # 查看本机ip，查看代理是否起作用
browser.get("http://httpbin.org/ip")
time.sleep(10)
browser.quit()
'''


'''
import pymysql
db = pymysql.connect('localhost','root','3.141592653579','chineseword',charset='utf8' )
cursor = db.cursor()
sql = "INSERT INTO table1(word) VALUES ('%s')" % ('新闻中心腾讯网资讯新闻财经房产视频科技腾讯网腾讯腾讯网从年创立至今已经成为集新闻信息区域垂直生活服务社会化媒体资讯和产品为一体的')

cursor.execute(sql)
db.commit()

response = requests.get('https://list.jd.com/list.html?cat=12218,12221&page=1')
print(response.text)

'''

'''
pattern = "[\u4e00-\u9fa5]+"
regex = re.compile(pattern)
results = regex.findall("<title>Scrapy分布式原理及Scrapy-Redis源码解析(待完善) - Cowry - CSDN博客</title>")
print(results)
'''

'''
req = Request(url='http://www.baidu.com?name=8&id=1',callback=lambda x:print(x),cookies={'k1':'vvvvv'})
result = request.request_fingerprint(req,include_headers=['cookies',])
print(result)
'''

'''
req = Request(url='http://www.baidu.com?id=1&name=8',callback=lambda x:print(x),cookies={'k1':666})
result = request.request_fingerprint(req,include_headers=['cookies',])
print(result)
'''

headers = {
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'referer': 'https://list.jd.com/list.html?cat=12218,12221',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
}

url = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds=4635062%2C5425142%2C4533171%2C2275209%2C5901356%2C100002807580%2C6159288%2C100001712403%2C5248452%2C100002807588%2C6405711%2C4968336%2C3820581%2C3699508%2C4635058%2C3491692%2C4927480%2C100001997041%2C5059844%2C4228126%2C6159262%2C6313732%2C7764173%2C100002392102%2C4176410%2C100002310798%2C100000795988%2C5752571%2C100001931899%2C6110976%2C5856728%2C5841987%2C100002445994%2C100000768781%2C3048509%2C4404739%2C100001809857%2C8094996%2C4635060%2C100000262695%2C5502768%2C2947731%2C2592301%2C5604668%2C3009387%2C100001931901%2C3680187%2C100002136408%2C5254604%2C4861382%2C100002419196%2C4213338%2C100000382987%2C7384607%2C4459535%2C6111066%2C3166514%2C2275211%2C5662261%2C3976754%2C3048505%2C&callback=jQuery9937512&_=1548229360349'
pattern = re.compile('\[.*]')
req = urllib.request.Request(url = url)
response = urllib.request.urlopen(req)
m = pattern.search(str(response.read().decode('GBK')))
print(m.group())
print(str(m.group()).replace('"','\''))
value = json.loads(m.group())
data1 = json.dumps(value)
data2 = json.loads(data1)
list = []
for item in data2:
    dict = {}
    try:
        dict['GoodCount'] = item['GoodCount']  # 好评
    except:
        print()
    try:
        dict['GeneralCount'] = item['GeneralCount']  # 中评
    except:
        print()
    try:
        dict['PoorCount'] = item['PoorCount']  # 差评
    except:
        print()
    try:
        dict['GoodRateShow'] = item['GoodRateShow']  # 分数
    except:
        print()
    list.append(dict)
print(list)


'''
url = 'https://ad.3.cn/ads/mgets?&callback=jQuery4190391&my=list_adWords&source=JDList&skuids=AD_4925701%2C'

pattern = re.compile('\[.*]')
response = urllib.request.urlopen(url)
m = pattern.search(str(response.read().decode('utf-8')))
value = json.loads(m.group())
data1 = json.dumps(value, ensure_ascii=False)
data2 = json.loads(data1)
list = []
for item in data2:
    dict = {}
    dict['ad'] = item['ad']
    list.append(dict)
print(list[0]['ad'])
'''
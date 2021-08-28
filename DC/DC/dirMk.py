# -*- coding: utf-8-*-
import hashlib
import os
import time
import re
# 获取指定名称的递归目录
from .settings import BASE_PATH

def get_dir_path(pathName):
    # 系统当前时间年份
    year = time.strftime('%Y', time.localtime(time.time()))
    # 月份
    month = time.strftime('%m', time.localtime(time.time()))
    # 日期
    day = time.strftime('%d', time.localtime(time.time()))
    # 小时
    hour = time.strftime('%H', time.localtime(time.time()))
    fileYear = BASE_PATH+ '/'+pathName + '/' + year
    fileDay = fileYear + '/' + month + '/' + day+'/'+hour
    if not os.path.exists(fileDay):
        os.makedirs(fileDay)

    return fileDay

def get_all_path(imgsrc,pathName='public/upload/goods'):
    cc = hashlib.md5(imgsrc.encode(encoding='UTF-8')).hexdigest()
    get_dir = get_dir_path(pathName)
    image_ext = imgsrc.split('.')[-1]
    image_name = cc+'.'+image_ext
    all_path = get_dir+'/'+image_name
    return all_path
def get_current_path():
    return os.getcwd()

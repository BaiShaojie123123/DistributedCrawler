# -*- coding: utf-8-*-
import hashlib


def calc_md5(passwd):
    md5 = hashlib.md5()     #获取一个md5加密算法对象
    md5.update(passwd.encode('utf-8'))
    ret = md5.hexdigest()
    return ret
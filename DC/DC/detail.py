import hashlib
import os
import time

from . import dirMk
from .DB import DB
from urllib import request

from .settings import BASE_PATH
from .strHelp import calc_md5


class detail(object):
    def __init__(self):
        return
    def process_item(self, item, spider):
        if spider.name!='JDDJ_Detail':
            return item
            print('爬取详情页')
        # 定义sql语句
        imgArr = item['imgArr']
        goods_id = item['goods_id']
        sourceType = item['source_type']



        for imgsrc in imgArr:

            imgsrc = imgsrc.replace('//','')
            all_path = dirMk.get_all_path(imgsrc)
            imgsrc = 'http://'+imgsrc
            imgsrc= imgsrc.replace('jfs/','s546x546_jfs/')



            goods_img = DB('tp_goods_images_spider')
            search_image_url = calc_md5(imgsrc)

            issetimg = goods_img.field('img_id').where([['goods_id','=',goods_id],['image_url_md5', '=', search_image_url]]).limit('1').fieldOne()
            insertPath = all_path.replace(BASE_PATH, '')
            if not issetimg:
                down = request.urlretrieve(imgsrc,all_path)
                if down:
                    image_insert = {
                        'image_url':insertPath,
                        'image_url_md5':search_image_url,
                        'source_url':imgsrc,
                        'goods_id':str(goods_id),
                        'source_type':str(sourceType)
                    }
                    goods_img.insert(image_insert)

        # # 判重按照商品 id  imgsrc
        # 判断 goods 表中首页图 original_img 是否有值,为空写入 有值不更改
        # tp_goods_spider = DB('tp_goods_spider')
        # original_img = tp_goods_spider.field('original_img').where(
        #     [['goods_id', '=', goods_id]]).limit('1').select()
        # if not original_img:
        #     update = {
        #         original_img: insertPath
        #     }
        #     tp_goods_spider.update()


        return item

    def __del__(self):
        # 关闭操作游标
        # self.cursor.close()
        # 关闭数据库连接
        # self.connection.close()
        return
    def calc_md5(self,passwd):
        md5 = hashlib.md5()     #获取一个md5加密算法对象
        md5.update(passwd.encode('utf-8'))
        ret = md5.hexdigest()
        return ret
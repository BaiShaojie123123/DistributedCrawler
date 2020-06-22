import hashlib
import os
import time

from . import dirMk
from .DB import DB
from urllib import request

from .settings import BASE_PATH
from .strHelp import calc_md5


class TextInfoPipeline(object):
    def __init__(self):
        return
    def process_item(self, item, spider):
        if spider.name!='JDDJ_url':
            return item
        print('爬取列表页数据清洗')
        # 定义sql语句
        sql = 1
        cc = item['name']
        imgsrc = item['imgsrc']
        imgsrc= imgsrc.replace('jfs/','s546x546_jfs/')
        all_path = dirMk.get_all_path(imgsrc)
        imgsrc = 'http://'+imgsrc
        search_image_url = calc_md5(imgsrc)

        goods_id = item['goods_id']
        sourceType = item['sourceType']
        goods_img = DB('tp_goods_images_spider')
        issetimg = goods_img.field('img_id').where([['goods_id','=',str(goods_id)],['image_url_md5', '=', search_image_url],['source_type','=',sourceType]]).limit('1').findOne()

        insertPath = all_path.replace(BASE_PATH, '')
        isGoodsImg = ''
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
                # goods_img.insert(image_insert)
                isGoodsImg = insertPath

        # # 判重按照商品 id  imgsrc
        # 判断 goods 表中首页图 original_img 是否有值,为空写入 有值不更改

        tp_goods_spider = DB('tp_goods_spider')
        goods = tp_goods_spider.where(
            [['goods_id', '=', goods_id]]).limit('1').findOne()
        if goods:
            if not goods['original_img']:
                print('图片为空')
                print('是这个商品的')
                update = {
                        'original_img': insertPath
                }
                tp_goods_spider.where([['goods_id','=',str(goods_id)]]).update(update)

        # 执行sql语句
        # self.cursor.execute(sql)
        # 保存修改
        # self.connection.commit()

        return item

    def __del__(self):
        # 关闭操作游标
        # self.cursor.close()
        # 关闭数据库连接
        # self.connection.close()
        return
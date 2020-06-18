# -*- coding: utf-8-*-
import pymysql
# # 建立数据库连接
# self.connection = pymysql.connect(host='127.0.0.1',
#                                   port=3306,
#                                   user='tpshopspider',
#                                   password='DtGKJFKrELs234n4',
#                                   db='tpshopspider',
#                                   charset='utf8')
# # 创建操作游标
# self.cursor = self.connection.cursor()
from .settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME


class DB:
    __host = MYSQL_HOST  # 服务器地址
    __username = MYSQL_USER  # 用户名
    __password = MYSQL_PASSWORD  # 密码
    __database = MYSQL_DB_NAME  # 数据库
    __field = '*'  # 查询字段
    __where = ''  # 条件
    __sql = False  # 是否返回sql
    __join = ''  # 联表
    __order = ''  # 排序
    __limit = ''  # 数量
    __offset = ''  # offset
    __fetchone = 0  # offset

    # 构造函数，在生成对象时调用
    def __init__(self, table):
        try:
            # 打开数据库连接 host, username, password, database
            self.db = pymysql.connect(self.__host, self.__username, self.__password, self.__database)
        except Exception as e:
            print(e)
            exit()

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        # self.cursor = self.db.cursor()
        self.table = table

    # 析构函数，释放对象时使用
    def __del__(self):
        try:
            # 关闭数据库连接
            self.db.close()
        except Exception as e:
            print(e)

    # 得到当前sql语句
    def getSql(self):
        self.__sql = True
        return self

    # 字段
    def field(self, str):
        self.__field = str
        return self

    # 联表
    def join(self, table, where):
        self.__join = ' LEFT JOIN ' + table + ' ON ' + where + ' '
        return self

    # 条件
    def where(self, param):
        self.__where = ' WHERE '
        if isinstance(param, list):
            for i in param:
                if isinstance(i[2], list):
                    tmp = '('
                    for j in i[2]:
                        tmp += str(j) + ','
                    tmp += ')'
                    self.__where += '`' + i[0] + '` ' + i[1] + ' ' + tmp + ' AND '
                else:
                    self.__where += '`' + i[0] + '` ' + i[1] + ' "' + str(i[2]) + '" AND '
            else:
                self.__where = self.__where[0:-4]
        else:
            self.__where += param

        return self

    # 排序
    def order(self, str):
        self.__order = ' ORDER BY ' + str
        return self

    # 数量
    def limit(self, str):
        self.__limit = ' LIMIT ' + str
        return self

    # 增加
    def insert(self, dict):
        key = value = ''
        for k, v in dict.items():
            key += '`' + k + '`,'
            value += '"' + str(v) + '",'

        key = key[0:-1]
        value = value[0:-1]

        sql = 'INSERT INTO ' + self.table + ' (' + key + ') VALUES (' + value + ')'
        print(sql)
        if self.__sql:
            return sql

        try:
            # 执行sql语句
            ret = self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return ret
        except Exception as e:
            # 如果发生错误则回滚
            self.db.rollback()
            print(e)
            return 0

    # 删除
    def delete(self):
        if self.__where:
            sql = "DELETE FROM " + self.table + self.__where
            if self.__sql:
                return sql

            try:
                # 执行sql语句
                ret = self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
                return ret
            except Exception as e:
                # 如果发生错误则回滚
                self.db.rollback()
                print(e)
                return 0

        else:
            raise BaseException('没有条件')  # 抛异常

    # 修改
    def update(self, dict):
        str_ = ''
        for k, v in dict.items():
            str_ += '`' + str(k) + '`="' + str(v) + '",'

        str_ = str_[0:-1]
        sql = 'UPDATE ' + self.table + ' SET ' + str_

        if self.__where:
            sql += self.__where
        if self.__sql:
            return sql

        try:
            # 执行sql语句
            ret = self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            return ret
        except Exception as e:
            # 如果发生错误则回滚
            self.db.rollback()
            print(e)
            return 0


    def getLastId(self):
        sql = "SELECT LAST_INSERT_ID()" + " FROM " + self.table
        if self.__sql:
            return sql
        # 使用 execute()  方法执行 SQL 查询
        return self.cursor.execute(sql)

    # 查询
    def offset(self, str):
        self.__offset = ' offset ' + str
        return self
    def findOne(self):
        return self.select(1)
    def findAll(self):
        return self.select(2)
    def fieldOne(self):
        data = self.select(1)
        if data:
            return data.popitem()[-1]
        else:
            return ''
    def select(self,type):
        sql = "SELECT " + self.__field + " FROM " + self.table

        if self.__join:
            sql += self.__join

        if self.__where:
            sql += self.__where

        if self.__order:
            sql += self.__order

        if self.__limit:
            sql += self.__limit
        if self.__offset:
            sql += self.__offset
        print(sql)
        if self.__sql:
            return sql

        # 使用 execute()  方法执行 SQL 查询

        self.cursor.execute(sql)
        if type==1:
            data = self.cursor.fetchone()
        else:
            # 使用 fetchall() 方法获取所有数据.
            data = self.cursor.fetchall()

        return data

#
# '''
# DROP TABLE IF EXISTS `people`;
# CREATE TABLE `people` (
#   `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '名字',
#   `sex` varchar(7) DEFAULT '' COMMENT '性别',
#   `job` varchar(6) DEFAULT '' COMMENT '工作',
#   `age` varchar(6) DEFAULT '' COMMENT '年龄',
#   `height` varchar(6) DEFAULT '' COMMENT '身高',
#   `weight` varchar(6) DEFAULT '' COMMENT '体重',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
# INSERT INTO `people` VALUES ('1', '赵一', '男', '学生', '8', '120', '35');
# INSERT INTO `people` VALUES ('2', '钱二', '女', '学生', '9', '111', '31');
# INSERT INTO `people` VALUES ('3', '孙三', '男', '学生', '10', '123', '34');
# INSERT INTO `people` VALUES ('4', '李四', '女', '学生', '11', '100', '30');
# '''
#
# db = DB('people')
#
# # 增加
# dict = {'name': '周五', 'sex': '男', 'job': '学生', 'age': '8', 'height': '121', 'weight': '32'}
# data = db.insert(dict)
# print(data)

# 删除
# data = db.where('id=6').delete()
# print(data)

# 修改
# dict = {'age': '9', 'height': '121', 'weight': '31'}
# data = db.where('id=7').update(dict)
# print(data)

# 查询 优化where条件 'id<11'
# data = db.field('id,name,age,job').where([['id', '>', 1]]).order('id desc').limit('3').select()


# -*- coding: UTF-8 -*-
# File:DBHelper.py
# Author:lmm
# Date:2018-04-10 16:37
# Description:数据库操作类

import pymysql
from company.items import CompanyItem, Location, Trade
from company import settings


MYSQL_HOST = settings.MYSQL_HOST
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWD = settings.MYSQL_PASSWD
MYSQL_DATABASE = settings.MYSQL_DATABASE


class DBHelper:

    @classmethod
    def save(cls, item):
        if isinstance(item, CompanyItem) and not DBHelper.existed(item['company_id']):
            sql = 'insert into company(company_id, name) values(%s,%s)'
            params = (item['company_id'], item['name'])
            db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute(sql, params)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
            db.close()

    @classmethod
    def existed(cls, company_id):
        sql = 'SELECT EXISTS(SELECT 1 FROM COMPANY WHERE company_id = %s)'
        params = (company_id)
        db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute(sql, params)
            re = cursor.fetchone()
            if re[0] == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
        db.close()

    @staticmethod
    def query_words():
        words = []
        sql = 'SELECT * FROM words WHERE deleted = 0'
        db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            re = cursor.fetchall()
            for row in re:
                words.append(row[1])
        except:
            pass
        db.close()
        return words

    @staticmethod
    def query_trade():
        trades = []
        sql = 'SELECT * FROM trade WHERE deleted = 0'
        db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            re = cursor.fetchall()
            for row in re:
                trade = Trade()
                trade.code = row[1]
                trade.name = row[2]
                trades.append(trade)
        except:
            pass
        db.close()
        return trades

    @staticmethod
    def query_location():
        locations = []
        sql = 'SELECT * FROM location WHERE deleted = 0'
        db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            re = cursor.fetchall()
            for row in re:
                loc = Location()
                loc.code = row[1]
                loc.name = row[2]
                locations.append(loc)
        except:
            pass
        db.close()
        return locations
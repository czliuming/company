# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from company.items import CompanyItem
from company.database.DBHelper import DBHelper
logger = logging.getLogger('CompanyPipeline')


class CompanyPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CompanyItem) and item['company_id']:
            DBHelper.save(item)
            logger.info('['+item['name']+']信息保存成功')
        else:
            pass
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    company_id = scrapy.Field()
    phones = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    note = scrapy.Field()
    pass

class BusInfoItem(scrapy.Item):
    # define the fields for your item here like:
    company_id = scrapy.Field()
    reg_num = scrapy.Field()
    credit_code = scrapy.Field()
    taxpayer_num = scrapy.Field()
    bus_term = scrapy.Field()
    reg_institute = scrapy.Field()
    reg_addr = scrapy.Field()
    org_num = scrapy.Field()
    company_type = scrapy.Field()
    category = scrapy.Field()
    audit_date = scrapy.Field()
    bus_scope = scrapy.Field()
    reg_capital = scrapy.Field()
    reg_time = scrapy.Field()
    company_state = scrapy.Field()
    legal_entity = scrapy.Field()
    legal_entity_type = scrapy.Field()
    pass

class HumanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    pass

class Location:
    code = ''
    name = ''
    level = 0
    parent = None
    children = []

class Trade:
    code = ''
    name = ''
    level = 0
    parent = None
    children = []
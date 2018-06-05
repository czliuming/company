# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.exceptions import CloseSpider

from company.database.DBHelper import DBHelper
from scrapy.http import Request
from company.items import CompanyItem
from urllib.parse import quote,unquote
import json


class TianyanchaSpider(scrapy.Spider):
    name = 'tianyancha'
    allowed_domains = ['tianyancha.com', 'www.tianyancha.com']
    start_urls = []
    cookies = []
    users = [
        {'mobile': '18526418908', 'cdpassword': '32e759bbd6bfcee89a29e3627ab81e65', 'login': False},
        {'mobile': '15620982875', 'cdpassword': '0ab44bd43d6b18fcd5cd928d6faab1b8', 'login': False}
    ]

    def start_requests(self):
        locations = DBHelper.query_location()
        words = DBHelper.query_words()
        for loc in locations:
            for word in words:
                url = 'https://' + loc.code + '.tianyancha.com/search?key=' + quote(word)
                yield Request(url, self.parse)

    def login(self, from_url='', call_back=None):
        if call_back is None:
            call_back = self.parse
        data = {'loginway': 'PL', 'autoLogin': True}
        url = 'https://www.tianyancha.com/cd/login.json'
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://www.tianyancha.com',
            'Referer': 'https://www.tianyancha.com/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4482.400 QQBrowser/9.7.13001.400',
            'X-Requested-With': 'XMLHttpRequest'
        }
        meta = {
            'from_url': from_url,
            'call_back': call_back,
        }
        for user in self.users:
            if not user['login']:
                data.update(user)
                meta['user'] = user['mobile']
                return Request(url, self.login_after, method='POST', headers=headers, body=json.dumps(data), meta=meta, dont_filter=True)


    def login_after(self, response):
        data = json.loads(response.body.decode(encoding='utf-8'))
        if data['state'] == 'ok':
            coo = response.headers.getlist('Set-Cookie')
            coo = (cookie.decode('utf-8').split(';', 1)[0] for cookie in coo)
            coo = [cookie.split('=') for cookie in coo]
            coo = dict(coo)
            coo['auth_token'] = data['data']['token']
            coo['user'] = response.meta['user']
            self.cookies.append(coo)
            self.logger.info('['+response.meta['user']+']登录成功！')
        for user in self.users:
            if(response.meta['user'] == user['mobile']):
                user['login'] = True
                break
        has_no_login = True
        for user in self.users:
            if not user['login']:
                has_no_login = False
                yield self.login(response.meta['from_url'], response.meta['call_back'])
        if has_no_login:
            yield Request(response.meta['from_url'], response.meta['call_back'], dont_filter=True)

    def parse(self, response):

        #判断是否已经登录
        if response.url.find('login') != -1:
            try:
                from_url = response.meta['redirect_urls'][0]
                yield self.login(from_url, self.parse)
            except:
                self.logger.error('['+response.url+']登录失败，请检查！')
                raise CloseSpider
        else:
            #抓取详细内容
            detail_tags = response.css('.query_name.sv-search-company')
            for detail_tag in detail_tags:
                detail_url = detail_tag.xpath('@href').extract()[0]
                if detail_url.find('company/') != -1:
                    company_id = detail_url[detail_url.index('company/')+8:]
                    if not DBHelper.existed(company_id):
                        yield Request(detail_url, self.parse_detail)

            #分页抓取
            page = 1
            url = response.url
            if re.search('search/p\d+?', url) is not None:
                page = url[url.index('search/p')+9:url.index('?')]
                try:
                    page = int(page)
                except:
                    pass
            page += 1
            if len(detail_tags) > 0:
                page_url = url[:url.index('search')+6]+'/p'+str(page)+url[url.index('?'):]
                yield Request(page_url, self.parse)

            #其他筛选条件抓取
            condition_tags = response.css('.pt8.pb8.pl10.sec-c2.codeSecName')
            for condition_tag in condition_tags:
                condition_url = condition_tag.xpath('@href').extract_first()
                yield Request(condition_url, self.parse)

    def parse_detail(self, response):
        item = CompanyItem()
        item['company_id'] = response.css('#_companyId::attr(value)').extract_first()
        item['name'] = response.css('#_companyName::attr(value)').extract_first()
        return item

# -*- coding: UTF-8 -*-
# File:proxy.py
# Author:lmm
# Date:2018-04-19 14:17
# Description:TODO

from urllib import request
import requests
import random
from company import settings
import json
import time
proxy_pool_host = settings.PROXY_POOL_HOST


class Proxy:

    ip_pool = set()

    @classmethod
    def get(cls):
        proxy_ip = ''
        if len(Proxy.ip_pool) > 0:
            ip_li = list(Proxy.ip_pool)
            ip = random.choice(ip_li)
            if Proxy.valid(ip):
                proxy_ip = ip
            else:
                Proxy.ip_pool.remove(ip)
                proxy_ip = Proxy.get()
            if len(Proxy.ip_pool) < 3:
                Proxy.process_pool()
        else:
            Proxy.process_pool()
            proxy_ip = Proxy.get()
        return proxy_ip

    @classmethod
    def process_pool(cls):
        ip_li = requests.get('http://'+proxy_pool_host+'/get_all').content.decode('utf-8')
        ip_li = json.loads(ip_li)
        for ip in ip_li:
            if Proxy.valid(ip):
                Proxy.ip_pool.add(ip)
            else:
                requests.get('http://'+proxy_pool_host+'/delete/?proxy={}'.format(ip))

    @classmethod
    def valid(cls, proxy_ip):
        if proxy_ip:
            try:
                proxies = {'http': proxy_ip,
                           'https': proxy_ip
                           }
                response = requests.get('https://tj.tianyancha.com/login', proxies=proxies, timeout=5)
                if response.status_code == 200 and response.text.find('登录') != -1:
                    return True
                else:
                    return False
            except Exception as e:
                return False

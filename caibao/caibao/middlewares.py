# -*- coding: utf-8 -*-
from utils.get_ua import *
# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals


class ProxyMid(object):
    def process_request(self, request, spider):
        spider.proxy = random.choice(spider.proxy_list)
        spider.logger.info('proxy:'+spider.proxy)
        request.meta['proxy'] = 'http://{}'.format(spider.proxy)


class RandomUserAgentMid(object):
    def process_request(self, request, spider):
        ua_list = [
            'Mozilla/5.0 (Linux; Android 5.1.1; SM-G960F Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36 Hexin_Gphone/9.58.07 (Royal Flush) hxtheme/1 innerversion/G037.08.296.1.32 userid/-460363742',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1']
        request.headers["User-Agent"] = random.choice(ua_list)

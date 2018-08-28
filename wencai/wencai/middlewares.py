# -*- coding: utf-8 -*-
from utils.get_ua import *
# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class RandomUserAgentMid(object):
    def process_request(self, request, spider):
        request.headers["User-Agent"] = get_ua()

class ProxyMid(object):
    def process_request(self, request, spider):
        if spider.name == 'shares_concept':
            spider.proxy = random.choice(spider.proxy_list)
            request.meta['proxy'] = 'http://{}'.format(spider.proxy)
            request.headers['Content-Type'] = 'application/json; charset=utf-8'
            # request.headers['Referer'] = 'http://www.iwencai.com/diag/block-detail?pid=8153&codes=000001&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D'
            # request.headers['Cookie'] = 'v=AjMBrqG6bKg7GiB8md8ZrWMWwjxeaMcqgfwLXuXQj9KJ5F0qbThXepHMm6z2'
        # request.meta['proxy'] = 'http://192.126.158.36:80'

# class CookieMid(object):
#     def process_request(self, request, spider):
#         print(reque)

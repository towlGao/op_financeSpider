# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random


def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


class RandomUserAgentMid(object):
    def process_request(self, request, spider):
        request.headers["User-Agent"] = get_ua()
        # request.meta['proxy'] = 'http://192.126.158.36:80'
        # if spider.name == 'szse_cp_notice':
        #     request.headers["Content-Type"] = "application/json"
        if spider.name == 'sse_cp_notice':
            request.headers['Referer'] = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'
            # ret = spider.pro_cs.execute('''select ip from proxy''')
            # ip_tuple = spider.pro_cs.fetchall()
            # index = random.randint(len(ip_tuple) - 1)
            # proxy_ip = ip_tuple[index][0]
            # request.meta['proxy'] = 'http://{}'.format(proxy_ip)


class ProxyMid(object):
    def process_request(self, request, spider):
        
        if spider.name in ['sse_cp_notice','sse_shares']:

            index = random.randint(0, len(spider.ip_tuple) - 1)

            proxy_ip = spider.ip_tuple[index][0]
            request.meta['proxy'] = 'http://{}'.format(proxy_ip)
        # request.meta['proxy'] = 'http://192.126.158.36:80'

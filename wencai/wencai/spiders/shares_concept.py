# -*- coding: utf-8 -*-
import scrapy
import json
import re
import random
from lxml import etree


class SharesConceptSpider(scrapy.Spider):
    name = 'shares_concept'
    allowed_domains = []
    start_urls = ['https://www.iwencai.com/stockpick']

    # start_urls = ['https://192.168.181.128:8080','https://192.168.181.128:8080','https://192.168.181.128:8080','https://192.168.181.128:8080','https://192.168.181.128:8080']



    def parse(self, response):
        shares = '000001'
        # for shares in self.shares_list:
        script_1 = '''
        function main(splash)
            splash:go("http://www.iwencai.com/diag/block-detail?pid=8153&codes=''' + shares + '''&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D")
            splash:wait(0.5)
            return {c=splash:get_cookies()}
        end
        '''

        script = '''
        function main(splash)
        splash:on_request(function(request)
            request:set_proxy{
            host = "''' + self.proxy.split(":")[0] + '''",
            port = ''' + self.proxy.split(":")[1] + ''',
        }
        end)
        assert(splash:go("http://www.iwencai.com/diag/block-detail?pid=8153&codes=''' + shares + '''&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D"))
        splash:wait(0.5)
        return {c=splash:get_cookies()}
        end
        '''
        # Cookie = response.request.headers.getlist('Cookie')
        # print('*'"40",Cookie) .format(self.proxy.split(":")[0],self.proxy.split(":")[1],shares)
        # flag = response.meta.get('flag') if response.meta.get('flag') else False
        basic_url = 'http://www.iwencai.com/diag/block-detail?pid=8153&codes={}&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D'
        if not self.shares_list:
            self.logger.error('股票列表获取失败', '*' * 100)
            return
        # for shares in self.shares_list:

        url = basic_url.format(shares[0])
        # yield scrapy.Request(url,callback=self.detail_parse)

        # callback = self.detail_parse if flag else self.parse
        yield scrapy.Request(url, callback=self.parse3, meta={
            'splash': {
                'endpoint': 'execute',
                'args': {'lua_source': script, 'wait': 15}
            },'shares':shares,
        }, dont_filter=True)

    def parse3(self,response):
        for shares in self.shares_list:
            if not self.shares_list.index(shares)%5:
                script = '''
                        function main(splash)
                        splash:on_request(function(request)
                            request:set_proxy{
                            host = "''' + self.proxy.split(":")[0] + '''",
                            port = ''' + self.proxy.split(":")[1] + ''',
                        }
                        end)
                        assert(splash:go("http://www.iwencai.com/diag/block-detail?pid=8153&codes=''' + shares + '''&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D"))
                        splash:wait(0.5)
                        return {c=splash:get_cookies()}
                        end
                        '''
                # Cookie = response.request.headers.getlist('Cookie')
                # print('*'"40",Cookie) .format(self.proxy.split(":")[0],self.proxy.split(":")[1],shares)
                # flag = response.meta.get('flag') if response.meta.get('flag') else False
                basic_url = 'http://www.iwencai.com/diag/block-detail?pid=8153&codes={}&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D'
                if not self.shares_list:
                    self.logger.error('股票列表获取失败', '*' * 100)
                    return
                # for shares in self.shares_list:

                url = basic_url.format(shares[0])
                # yield scrapy.Request(url,callback=self.detail_parse)

                # callback = self.detail_parse if flag else self.parse
                yield scrapy.Request(url, callback=self.parse2, meta={
                    'splash': {
                        'endpoint': 'execute',
                        'args': {'lua_source': script, 'wait': 15}
                    }, 'shares': shares,
                }, dont_filter=True)
            else:
                basic_url = 'http://www.iwencai.com/diag/block-detail?pid=8153&codes={}&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D'

                cookies = json.loads(response.body.decode())
                # cook = ';'.join([cookie['name']+'='+cookie['value'] for cookie in cookies if cookie['name'] != 'vvvv'])
                # self.cook = cook
                cook = {cookie['name']: cookie['value'] for cookie in cookies if cookie['name'] == 'v'}
                yield scrapy.Request(basic_url.format(shares), cookies=cook, callback=self.detail_parse, meta={'shares': shares})

    def parse2(self, response):
        basic_url = 'http://www.iwencai.com/diag/block-detail?pid=8153&codes={}&codeType=stock&info=%7B%22view%22%3A%7B%22nolazy%22%3A1%2C%22parseArr%22%3A%7B%22_v%22%3A%22new%22%2C%22dateRange%22%3A%5B%5D%2C%22staying%22%3A%5B%5D%2C%22queryCompare%22%3A%5B%5D%2C%22comparesOfIndex%22%3A%5B%5D%7D%2C%22asyncParams%22%3A%7B%22tid%22%3A137%7D%7D%7D'

        shares = response.meta['shares']
        url = basic_url.format(shares)
        # Cookie = response.request.headers.getlist('Cookie')
        # print('*'"40", Cookie)
        print(response.body.decode())
        cookies = json.loads(response.body.decode())
        # cook = ';'.join([cookie['name']+'='+cookie['value'] for cookie in cookies if cookie['name'] != 'vvvv'])
        # self.cook = cook
        cook = {cookie['name']: cookie['value'] for cookie in cookies if cookie['name'] == 'v'}
        print(cook)
        yield scrapy.Request(url, cookies=cook, callback=self.detail_parse,meta={'shares':shares})

    def detail_parse(self, response):
        shares = response.meta['shares']
        content = response.body.decode()
        html_data = json.loads(content)
        html_data = html_data['data']['data']['tableTempl']
        html = etree.HTML(html_data)
        product = html.xpath('//td[@colnum="4"]/div/span/a/text()')
        concept = html.xpath('//td[@colnum="5"]/div/span/a/text()')
        yield {'product': product, 'concept': concept,'code':shares}

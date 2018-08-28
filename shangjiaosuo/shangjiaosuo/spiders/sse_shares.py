# -*- coding: utf-8 -*-
# -*- create by gt 18-8-9 -*-
import time
import scrapy
import json
import re


class SseSharesSpider(scrapy.Spider):
    name = 'sse_shares'
    allowed_domains = ['sse.com.cn']
    start_urls = [
        'http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin=0&end=25&_={}'.format(
            int(time.time() * 1000))]

    def parse(self, response):
        '''获取第一页数据'''
        json_data = json.loads(response.body.decode('gbk'))
        total_page = json_data['total']
        basic_url = 'http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code%2Cname%2Copen%2Chigh%2Clow%2Clast%2Cprev_close%2Cchg_rate%2Cvolume%2Camount%2Ctradephase%2Cchange%2Camp_rate&order=&begin={}&end={}&_={}'
        for i in range(total_page // 25 + 1):
            item = {}
            begin = i * 25
            end = (i + 1) * 25
            next_url = basic_url.format(begin, end, int(time.time() * 1000))
            yield scrapy.Request(
                next_url,
                callback=self.list_parse,
                meta={'item': item}
            )

    def list_parse(self, response):
        item = response.meta['item']
        json_data = json.loads(response.body.decode('gbk'))
        data = json_data['list']
        print(data)
        for shares in data:
            item['shares_code'] = shares[0]
            item['shares_name'] = shares[1]
            detail_url = 'http://query.sse.com.cn/commonQuery.do?isPagination=false&sqlId=COMMON_SSE_ZQPZ_GP_GPLB_C&productid={}&_={}'
            yield scrapy.Request(
                detail_url.format(item['shares_code'], int(time.time() * 1000)),
                callback=self.detail_parse,
                meta={'item': item},
                headers={'Referer': 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE={}'.format(item['shares_code'])}
            )

    def detail_parse(self, response):

        item = response.meta['item']
        json_data = json.loads(response.body.decode())
        result = json_data['result']
        print(result)
        if result:
            result = result[0]
        item['company_name_short'] = result['COMPANY_ABBR']
        item['company_code'] = result['COMPANY_CODE']
        item['industry'] = result['CSRC_CODE_DESC']
        item['shares_code_A'] = None if result['SECURITY_CODE_A'] == '-' else result['SECURITY_CODE_A']
        item['shares_name_A'] = None if result['SECURITY_ABBR_A'] == '-' else result['SECURITY_ABBR_A']
        item['shares_code_B'] = None if result['SECURITY_CODE_B'] == '-' else result['SECURITY_CODE_B']
        item['shares_name_B'] = None if result['SECURITY_CODE_B'] == '-' else result['COMPANY_ABBR']
        item['company_detail_url'] = response.url
        item['exchange'] = '上交所'
        # yield item
        print(item)
# -*- coding: utf-8 -*-
import scrapy
import re
import json


class SzseSharesSpider(scrapy.Spider):
    name = 'szse_shares'
    allowed_domains = ['szse.cn']
    start_urls = ['http://www.szse.cn/api/report/ShowReport/data?CATALOGID=1110&TABKEY=tab1',
                  'http://www.szse.cn/api/report/ShowReport/data?CATALOGID=1110&TABKEY=tab2']

    def parse(self, response):
        data_list = response.body.decode()
        data_list = json.loads(data_list)
        data_dict = [i for i in data_list if i['data']]
        data_dict = data_dict[0] if data_dict else None
        if not data_dict:
            return
        item = {}
        shares_list = data_dict['data']
        for shares in shares_list:
            item['company_code'] = shares['zqdm']
            item['shares_code_B'] = shares.get('bgdm', None)
            item['shares_name_B'] = shares.get('bgjc', None)
            item['shares_code_A'] = shares.get('agdm', None)
            item['shares_name_A'] = shares.get('agjc', None)
            item['industry'] = shares['sshymc']
            company_info = shares['gsjc']
            # print(company_info)
            company_name = re.findall(r'<u>(.+?)</u>', company_info)[0]
            company_detail_url = re.findall(r"<a href='(.+?)' target=", company_info)[0]
            item['company_name_short'] = company_name
            item['company_detail_url'] = company_detail_url
            # print(item)
            yield item
        # 翻页
        current_page = re.findall(r'PAGENO=(\d+)', response.url)
        current_page = int(current_page[0]) if current_page else 1
        next_current_page = current_page + 1
        # print("*"*100,current_page)
        page = re.findall(r'PAGENO=\d+', response.url)
        if page:
            next_url = re.sub(r'PAGENO=\d+', 'PAGENO={}'.format(next_current_page), response.url)
        else:
            next_url = response.url + '&PAGENO={}'.format(next_current_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse
        )

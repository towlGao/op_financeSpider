# -*- coding: utf-8 -*-
import scrapy
from pprint import pprint


class FinanceInfoSpider(scrapy.Spider):
    name = 'finance_info'
    allowed_domains = []
    start_urls = ['https://basic.10jqka.com.cn/mobile/ajax/finance/000001/maintablen/year']

    def parse(self, response):
        basic_url = 'https://basic.10jqka.com.cn/mobile/ajax/finance/{}/maintablen/{}'
        # self.shares_list = ['000001']
        for share in self.shares_list:
            yield scrapy.Request(basic_url.format(share, 'all'), meta={'shares': share, 'flag': 'all'},
                                 callback=self.detail_parse,dont_filter=True)
            yield scrapy.Request(basic_url.format(share, 'year'), meta={'shares': share, 'flag': 'year'},
                                 callback=self.detail_parse,dont_filter=True)
            # yield basic_url.format(shares, 'year')

    def detail_parse(self, response):
        # print(11111)
        share = response.meta['shares']
        flag = response.meta['flag']
        item = {}
        if flag == 'all':
            item['type'] = '最新'
        if flag == 'year':
            item['type'] = '年报'
        div_list = response.xpath('//div[@id="right_area"]/div/div[@class="block-holder"]')
        odd_div_list = response.xpath('//div[@id="right_area"]/div/div[@class="block-holder odd hide"]')
        if not div_list:
            self.logger.error('未爬取到数据(被封)')
            self.logger.error(response.body.decode())
        for div_index in range(len(div_list)):
            # print(div_index)
            div = div_list[div_index]
            # 股票代码
            item['code'] = share
            # 指标年份
            item['year'] = div.xpath('./div[1]/span/text()').extract_first()
            # 营业收入
            item['revenue'] = div.xpath('./div[2]/ul/li[1]/text()').extract_first().strip()
            # 净利润
            item['net_profit'] = div.xpath('./div[2]/ul/li[2]/text()').extract_first().strip()
            # 扣非净利润
            item['un_net_profit'] = div.xpath('./div[2]/ul/li[3]/text()').extract_first().strip()
            # 每股收益
            item['asset_per_share'] = div.xpath('./div[3]/ul/li[1]/text()').extract_first().strip()
            # 每股净资产
            item['asset_value_per_share'] = div.xpath('./div[3]/ul/li[2]/text()').extract_first().strip()
            # 每股资本公积金
            item['accu_fund_per_share'] = div.xpath('./div[3]/ul/li[3]/text()').extract_first().strip()
            # 每股未分配利润
            item['retained_profit_per_share'] = div.xpath('./div[3]/ul/li[4]/text()').extract_first().strip()
            # 每股经营现金流
            item['cash_flow_per_share'] = div.xpath('./div[3]/ul/li[5]/text()').extract_first().strip()
            # 净资产收益率
            item['return_on_equity'] = div.xpath('./div[4]/ul/li[1]/text()').extract_first().strip()
            # 净资产收益率-摊薄
            item['return_on_equity_diminish'] = div.xpath('./div[4]/ul/li[2]/text()').extract_first().strip()
            # 资产负债率
            item['asset_liability_ratio'] = div.xpath('./div[5]/ul/li/text()').extract_first().strip()
            # 净利润同比增长率
            item['net_profit_compared_growth'] = div.xpath('./div[6]/ul/li[1]/text()').extract_first().strip()
            # 营业收入同比增长率
            item['revenue_compared_growth'] = div.xpath('./div[6]/ul/li[2]/text()').extract_first().strip()
            # 同比
            odd_div = odd_div_list[div_index]
            # 营业收入
            item['revenue_YOY'] = odd_div.xpath('./div[2]/ul/li[1]/text()').extract_first().strip()
            # 净利润
            item['net_profit_YOY'] = odd_div.xpath('./div[2]/ul/li[2]/text()').extract_first().strip()
            # 扣非净利润
            item['un_net_profit_YOY'] = odd_div.xpath('./div[2]/ul/li[3]/text()').extract_first().strip()
            # 每股收益
            item['asset_per_share_YOY'] = odd_div.xpath('./div[3]/ul/li[1]/text()').extract_first().strip()
            # 每股净资产
            item['asset_value_per_share_YOY'] = odd_div.xpath('./div[3]/ul/li[2]/text()').extract_first().strip()
            # 每股资本公积金
            item['accu_fund_per_share_YOY'] = odd_div.xpath('./div[3]/ul/li[3]/text()').extract_first().strip()
            # 每股未分配利润
            item['retained_profit_per_share_YOY'] = odd_div.xpath('./div[3]/ul/li[4]/text()').extract_first().strip()
            # 每股经营现金流
            item['cash_flow_per_share_YOY'] = odd_div.xpath('./div[3]/ul/li[5]/text()').extract_first().strip()
            # 净资产收益率
            item['return_on_equity_YOY'] = odd_div.xpath('./div[4]/ul/li[1]/text()').extract_first().strip()
            # 净资产收益率-摊薄
            item['return_on_equity_diminish_YOY'] = odd_div.xpath('./div[4]/ul/li[2]/text()').extract_first().strip()
            # 资产负债率
            item['asset_liability_ratio_YOY'] = odd_div.xpath('./div[5]/ul/li/text()').extract_first().strip()
            # 净利润同比增长率
            item['net_profit_compared_growth_YOY'] = odd_div.xpath('./div[6]/ul/li[1]/text()').extract_first().strip()
            # 营业收入同比增长率
            item['revenue_compared_growth_YOY'] = odd_div.xpath('./div[6]/ul/li[2]/text()').extract_first().strip()
            yield item
            # pprint(item)
            # item['revenue_YOY'] =
            # item['net_profit_YOY'] =
            # item['un_net_profit_YOY'] =
            # item['asset_per_share_YOY'] =
            # item['asset_value_per_share_YOY'] =
            # item['accu_fund_per_share_YOY'] =
            # item['retained_profit_per_share_YOY'] =
            # item['cash_flow_per_share_YOY'] =
            # item['return_on_equity_YOY'] =
            # item['return_on_equity_diminish_YOY'] =
            # item['asset_liability_ratio_YOY'] =
            # item['net_profit_compared_growth_YOY'] =
            # item['revenue_compared_growth_YOY'] =

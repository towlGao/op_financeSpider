# -*- coding: utf-8 -*-
from utils.connect_mysql import *
from caibao.settings import *
from utils.proxy import *
from utils.get_time import *
import re


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CaibaoPipeline(object):
    def process_item(self, item, spider):
        type_ = item['type']
        year = item['year']
        result = re.findall(r'\s', year)
        year = re.sub(r'\s', '', year) if result else year
        share_code = item['code']
        revenue = item['revenue']
        net_profit = item['net_profit']
        un_net_profit = item['un_net_profit']
        aps = item['asset_per_share']
        avps = item['asset_value_per_share']
        afps = item['accu_fund_per_share']
        rpps = item['retained_profit_per_share']
        cfps = item['cash_flow_per_share']
        roe = item['return_on_equity']
        roed = item['return_on_equity_diminish']
        alr = item['asset_liability_ratio']
        npcg = item['net_profit_compared_growth']
        rcg = item['revenue_compared_growth']
        revenue_YOY = item['revenue_YOY']
        net_profit_YOY = item['net_profit_YOY']
        un_net_profit_YOY = item['un_net_profit_YOY']
        apsy = item['asset_per_share_YOY']
        avpsy = item['asset_value_per_share_YOY']
        afpsy = item['accu_fund_per_share_YOY']
        rppsy = item['retained_profit_per_share_YOY']
        cfpsy = item['cash_flow_per_share_YOY']
        roey = item['return_on_equity_YOY']
        roedy = item['return_on_equity_diminish_YOY']
        alry = item['asset_liability_ratio_YOY']
        npcgy = item['net_profit_compared_growth_YOY']
        rcgy = item['revenue_compared_growth_YOY']
        create_time = get_time().split(" ")[0]
        update_time = get_time().split(" ")[0]
        column = ['revenue', 'net_profit', 'un_net_profit', 'asset_per_share', 'asset_value_per_share',
                  'accu_fund_per_share', 'retained_profit_per_share', 'cash_flow_per_share', 'return_on_equity',
                  'return_on_equity_diminish', 'asset_liability_ratio', 'net_profit_compared_growth',
                  'revenue_compared_growth', 'revenue_YOY', 'net_profit_YOY', 'un_net_profit_YOY',
                  'asset_per_share_YOY', 'asset_value_per_share_YOY', 'accu_fund_per_share_YOY',
                  'retained_profit_per_share_YOY', 'cash_flow_per_share_YOY', 'return_on_equity_YOY',
                  'return_on_equity_diminish_YOY', 'asset_liability_ratio_YOY', 'net_profit_compared_growth_YOY',
                  'revenue_compared_growth_YOY','type','create_time','update_time']
        data = (
            0, share_code, year, revenue, net_profit, un_net_profit, aps, avps, afps, rpps, cfps, roe, roed, alr, npcg,
            rcg,
            revenue_YOY, net_profit_YOY, un_net_profit_YOY, apsy, avpsy, afpsy, rppsy, cfpsy, roey, roedy, alry, npcgy,
            rcgy, type_, create_time, update_time)
        # print(data)
        ret2, ret3 = check_db(spider.cs, [share_code, year], 'finance_info')
        if not ret2:
            insert_data(spider.db, spider.cs, data, 'finance_info')
        else:
            update_data(spider.db, spider.cs, [column, data])
        return item

    def open_spider(self, spider):
        db, cs = connect_mysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE)
        spider.db = db
        spider.cs = cs
        pro_db, pro_cs = connect_mysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, PROXY_DB)

        spider.pro_db = pro_db
        spider.pro_cs = pro_cs
        ip_tuple = get_proxy(spider.pro_cs)
        spider.proxy_list = ip_tuple
        shares = get_shares(spider.cs)
        shares = [i for i in shares if i] if shares else None
        # finished_code = finished_shares(spider.cs)
        # shares = set(shares) - set(finished_code)
        spider.shares_list = shares if shares else None

    def close_spider(self, spider):
        spider.cs.close()
        spider.db.close()
        spider.pro_db.close()
        spider.pro_cs.close()

# -*- coding: utf-8 -*-
from utils.connect_mysql import *
from utils.proxy import *
from utils import check_file
from wencai.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, PROXY_DB, MYSQL_DATABASE
# Define your item pipelines here
# from selenium import webdriver
import time
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WencaiPipeline(object):
    def process_item(self, item, spider):
        code, product, concept = [item['code'],item['product'],item['concept']]

        for pro in product:
            ret1 = check_db1(spider.cs,pro, 'is_product=1', 1)
            if not ret1:
                pro_data = (0, pro, 1, None)
                pro_insert_sql = '''insert into `product&concept` value %s'''
                spider.cs.execute(pro_insert_sql, [pro_data])
                spider.db.commit()

            spider.cs.execute('''select id from `product&concept` where name=%s''', [pro])
            pro_id = spider.cs.fetchone()[0]
            insert_id = (0, code, pro_id)
            ret2 = check_db1(spider.cs,pro, 'product_id={}'.format(pro_id), 3)
            if not ret2:
                pro_sql = '''insert into company_product value %s'''
                spider.cs.execute(pro_sql, [insert_id])
                spider.db.commit()
        for con in concept:
            ret1 = check_db1(spider.cs,con, 'is_concept=1', 1)
            if not ret1:
                con_data = (0, con, None, 1)
                con_insert_sql = '''insert into `product&concept` value %s'''
                spider.cs.execute(con_insert_sql, [con_data])
                spider.db.commit()
            spider.cs.execute('''select id from `product&concept` where name=%s''', [con])
            con_id = spider.cs.fetchone()[0]
            insert_id1 = (0, code, con_id)
            ret2 = check_db1(spider.cs,con, 'concept_id={}'.format(con_id), 2)
            if not ret2:
                con_sql = '''insert into company_concept value %s'''
                spider.cs.execute(con_sql, [insert_id1])
                spider.db.commit()
        return item


    def open_spider(self, spider):
        '''开启爬虫执行一次'''
        if spider.name == 'shares_concept':
            pro_db, pro_cs = connect_mysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, PROXY_DB)

            spider.pro_db = pro_db
            spider.pro_cs = pro_cs
            ip_tuple = get_proxy(spider.pro_cs)
            spider.proxy_list = ip_tuple
            # print(spider.ip_tuple)
        db, cs = connect_mysql(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,MYSQL_DATABASE)
        check_file.check_log('shares_concept.log')

        spider.db = db
        spider.cs = cs
        shares = get_shares(spider.cs)
        # finished_code = finished_shares(spider.cs)
        # shares = set(shares) - set(finished_code)
        spider.shares_list = shares if shares else None

    def close_spider(self, spider):
        '''关闭爬虫执行一次'''
        spider.cs.close()
        spider.db.close()
        # spider.browser.close()
        if spider.name == 'shares_concept':

            spider.pro_cs.close()
            spider.pro_db.close()
        spider.logger.info("当前为最后一次爬虫结束时间：%s" % time.ctime())

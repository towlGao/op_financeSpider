# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from shenjiaosuo.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, EXCHANGE_TABLE_NAME, \
    COMPANY_TABLE_NAME, PROXY_DB, SHARES_TABLE_NAME
from utils.connect_mysql import *
from utils.get_time import *
from utils import check_file
import time
import re


class ShenjiaosuoPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'szse_notice':
            '''深交所公告处理'''

            l1_title = item.get('l1_title')
            l2_title = item.get('l2_title')
            title = item.get('title')
            l3_sub_title = item.get('l3_sub_title')

            detail_url = item.get('detail_url')
            doc_type = item.get('doc_type')
            content = item.get('content')
            if content:
                temp = content.pop()
                temp = re.sub(r'\w{4}年\w+?月\w+?日', '', temp)
                if temp:
                    content.append(temp)

            table_content = item.get('table_content')

            table_content = json.dumps(table_content) if table_content else None

            appendix_path_list = item.get('appendix_path_list')
            appendix_path_list = json.dumps(appendix_path_list) if appendix_path_list else None

            release_time = item.get('release_time') if item.get('release_time') else None
            release_time = release_time if release_time else item.get('release_time_l')
            notice_time = item.get('notice_time')
            if notice_time:
                if not re.findall(r'\d+', notice_time):
                    notice_time = None
            if not any([notice_time, release_time]):
                notice_time = None
                release_time = None
            elif notice_time is None and release_time:
                notice_time = release_time
            elif release_time is None and notice_time:
                release_time = notice_time
            else:
                pass
            if release_time:
                release_time = release_time.split('-')
                release_time = '-'.join([t.zfill(2) for t in release_time])
            create_time = get_time()
            update_time = get_time()
            content = json.dumps(content) if content else None

            data = (0, l1_title, l2_title, title, l3_sub_title, detail_url, doc_type, content, table_content,
                    appendix_path_list, release_time, notice_time, create_time, update_time)
            # data = (0, l1_title, l2_title, title, detail_url, doc_type, content, l3_sub_title, table_content,
            #        appendix_path_list, release_time, notice_time, create_time, update_time)
            ret2, ret3 = check_db(spider.cs, detail_url, EXCHANGE_TABLE_NAME)
            # 如果ret2有值 则表示在数据库中存在该数据，不需要继续存储
            ret = insert_data(spider.db, spider.cs, (data,), EXCHANGE_TABLE_NAME) if not ret2 else 0

            if not any([ret, ret2]):
                spider.logger.error("%s: 存储失败 %s " % (time.time(), str(data) + "*" * 100))

        if spider.name == 'szse_cp_notice':
            '''上市公司公告处理'''
            start_time = time.time()
            handle_time = item.get("handle_time", None)
            l1_title = item.get('l1_title')
            l2_title = item.get('l2_title')
            title = item.get('title')
            category = item.get('category')
            sec_code = item.get('sec_code')
            sec_name = item.get('sec_name')
            publish_time = item.get('publish_time')
            publish_time = publish_time.split(" ")[0]
            appendix_path = item.get('appendix_path')
            appendix_path = json.dumps(appendix_path) if appendix_path else None

            detail_url = item.get('detail_url')
            doc_type = item.get('doc_type')
            content = item.get('content')
            content = json.dumps(content) if content else None
            create_time = get_time()
            update_time = get_time()
            data = (0, l1_title, l2_title, title, category, sec_code, sec_name, publish_time, appendix_path, detail_url,
                    doc_type, content, create_time, update_time)
            ret2, ret3 = check_db(spider.cs, detail_url, COMPANY_TABLE_NAME)
            ret = insert_data(spider.db, spider.cs, (data,), COMPANY_TABLE_NAME) if not ret2 else 0
            if not any([ret, ret2]):
                spider.logger.error("%s: 存储失败 %s " % (time.time(), str(data) + "*" * 100))
            end_time = time.time()
            h_time = end_time - start_time
            if h_time + handle_time[1] > handle_time[0]:
                spider.logger.info("%s,%s" % (h_time + handle_time[1], handle_time[0]))

        if spider.name == 'szse_shares':
            company_code = item['company_code']
            shares_code_A = item['shares_code_A']
            shares_name_A = item['shares_name_A']
            shares_code_B = item['shares_code_B']
            shares_name_B = item['shares_name_B']
            industry = item['industry']
            company_name_short = item['company_name_short']
            company_detail_url = item['company_detail_url']
            ret2, ret3 = check_db(spider.cs, company_code, SHARES_TABLE_NAME)
            print(ret2, ret3)
            if shares_code_A and not shares_code_B:
                column = (
                    'company_code', 'company_abbreviated', 'shares_code_A', 'shares_name_A', 'industry',
                    'detail_url_in_exchange', 'exchange',
                    'create_time', 'update_time')
                data = (
                    company_code, company_name_short, shares_code_A, shares_name_A, industry, company_detail_url, '深交所',
                    get_time(), get_time())
                check_data = (company_code, company_name_short, shares_name_A)
                # ret4 = [ret3[1], ret3[2], ret3[4]] if ret3 else None
                # if ret4 and ret4[1] != check_data[1]:
                #     # 公司简称变化
                #     column = ('company_code', 'company_abbreviated')
                #     data = (ret4[0], ret4[1])
                #     new_data = (check_data[0],check_data[1])
                #     change_company_name(spider.db,spider.cs,column,data)
                # elif ret4 and ret4[2] != check_data[2]:
                #     # a股简称变化
                #     column = ('company_code', 'shares_name_A')
                #     data = (ret4[0], ret4[2])
                #     new_data = (check_data[0], check_data[2])
                #     change_company_name(spider.db,spider.cs,column,data)
                # elif not ret4:
                #     # 新股上市
                #     update_data(spider.db,spider.cs,(('company_code','is_new'),(company_code,1)))

                params = (column, data)
                # update_data(spider.db, spider.cs, params, SHARES_TABLE_NAME)

            elif not shares_code_A and shares_code_B:
                column = (
                    'company_code', 'company_abbreviated', 'shares_code_B', 'shares_name_B', 'industry',
                    'detail_url_in_exchange', 'exchange',
                    'create_time', 'update_time')
                data = (
                    company_code, company_name_short, shares_code_B, shares_name_B, industry, company_detail_url, '深交所',
                    get_time(), get_time())
                check_data = (company_code, company_name_short, shares_name_B)
                # ret4 = [ret3[1], ret3[2], ret3[6]] if ret3 else None
                # if ret4 and ret4[1] != check_data[1]:
                #     # 公司简称变化
                #     column = ('company_code', 'company_abbreviated')
                #     data = (ret4[0], ret4[1])
                #     new_data = (check_data[0], check_data[1])
                #     change_company_name(spider.db,spider.cs,column,data)

                # elif ret4 and ret4[2] != check_data[2]:
                #     # b股简称变化
                #     column = ('company_code', 'shares_name_B')
                #     data = (ret4[0], ret4[2])
                #     new_data = (check_data[0], check_data[2])
                #     change_company_name(spider.db,spider.cs,column,data)
                # elif not ret4:
                #     # 新股上市
                #     update_data(spider.db,spider.cs,(('company_code','is_new'),(company_code,1)))

                params = (column, data)
                # update_data(spider.db, spider.cs, params, SHARES_TABLE_NAME)
            if ret2:
                update_data(spider.db, spider.cs, params)
            else:
                # print('insert',"*"*100)
                # print(params)
                # print('insert', "-" * 100)
                ret = insert_data(spider.db, spider.cs, params, SHARES_TABLE_NAME)
                print(ret)

        return item

    def open_spider(self, spider):
        '''开启爬虫执行一次'''
        db, cs = connect_mysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE)
        check_file.check_log('szse_notice.log')
        check_file.check_log('szse_cp_notice.log')
        spider.db = db
        spider.cs = cs
        # 设置代理
        # pro_db, pro_cs = connect_mysql(MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWD,PROXY_DB)
        # spider.pro_db = pro_db
        # spider.pro_cs = pro_cs

    def close_spider(self, spider):
        '''关闭爬虫执行一次'''
        # if spider.name == 'szse_shares':
        #     is_delete(spider.db, spider.cs)
        spider.cs.close()
        spider.db.close()
        # spider.pro_cs.close()
        # spider.pro_db.close()
        spider.logger.info("当前为最后一次爬虫结束时间：%s" % time.ctime())


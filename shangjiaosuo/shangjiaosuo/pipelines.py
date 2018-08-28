# -*- coding: utf-8 -*-
import json
from pymongo import MongoClient
from shangjiaosuo.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, EXCHANGE_TABLE_NAME, \
    COMPANY_TABLE_NAME, PROXY_DB, SHARES_TABLE_NAME
from utils.connect_mysql import *
from utils.get_time import *
from utils import check_file
from utils.proxy import *


class ShangjiaosuoPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'sse_notice':
            item['appendix_list'] = item['appendix_list'] if item['appendix_list'] else None
            # print(item)
            l1_title = '上交所公告'
            l2_title = item['l2_title']
            title = item['title']
            cp_code = None
            detail_url = item['detail_url']
            doc_type = item['detail_url'].rsplit(".", 1)[1]
            content = item['content']
            content = json.dumps(content) if content else None
            table_content = None
            appendix_path_list = item['appendix_list']
            appendix_path_list = json.dumps(appendix_path_list) if appendix_path_list else None
            release_time = item['release_time']
            notice_time = item['notice_time']
            create_time = get_time()
            update_time = get_time()
            data = (0, l1_title, l2_title, title, cp_code, detail_url, doc_type, content, table_content,
                    appendix_path_list, release_time, notice_time, create_time, update_time)

            ret2 = check_db(spider.cs, detail_url, EXCHANGE_TABLE_NAME)
            # 如果ret2有值 则表示在数据库中存在该数据，不需要继续存储
            ret = insert_data(spider.db, spider.cs, data, EXCHANGE_TABLE_NAME) if not ret2 else 0

            if not any([ret, ret2]):
                spider.logger.error("%s: 存储失败 %s " % (time.ctime(), str(data) + "*" * 100))

        if spider.name == 'sse_cp_notice':
            l1_title = item['l1_title']
            l2_title = item['l2_title']
            title = item['title']
            category = item['category']
            sec_code = item['sec_code']
            sec_name = item['sec_name']
            publish_time = item['publish_time']
            appendix_path_list = item['appendix_path_list']
            appendix_path_list = appendix_path_list if appendix_path_list else None
            detail_url = item['detail_url']
            doc_type = item['doc_type']
            content = item['content']
            create_time = get_time()
            update_time = get_time()

            data = (
                0, l1_title, l2_title, title, category, sec_code, sec_name, publish_time, appendix_path_list,
                detail_url,
                doc_type, content, create_time, update_time)
            # data = (
            # 0, l1_title, l2_title, title)
            ret2,ret3 = check_db(spider.cs, detail_url, COMPANY_TABLE_NAME)
            # 如果ret2有值 则表示在数据库中存在该数据，不需要继续存储

            ret = insert_data(spider.db, spider.cs, data, COMPANY_TABLE_NAME) if not ret2 else 0

            if not any([ret, ret2]):
                spider.logger.error("%s: 存储失败 %s " % (time.ctime(), str(data) + "*" * 100))

        if spider.name == 'sse_shares':
            company_code = item['company_code']
            shares_code_A = item['shares_code_A']
            shares_name_A = item['shares_name_A']
            shares_code_B = item['shares_code_B']
            shares_name_B = item['shares_name_B']
            industry = item['industry']
            company_name_short = item['company_name_short']
            company_detail_url = item['company_detail_url']
            ret2, ret3 = check_db(spider.cs, company_code, SHARES_TABLE_NAME)
            # print(ret2, ret3)
            if shares_code_A and not shares_code_B:
                column = (
                    'company_code', 'company_abbreviated', 'shares_code_A', 'shares_name_A', 'industry',
                    'detail_url_in_exchange', 'exchange',
                    'create_time', 'update_time')
                data = (
                    company_code, company_name_short, shares_code_A, shares_name_A, industry, company_detail_url,
                    '上交所',
                    get_time(), get_time())
                check_data = (company_code, company_name_short, shares_name_A)
                ret4 = [ret3[1], ret3[2], ret3[4]] if ret3 else None
                if ret4 and ret4[1] != check_data[1]:
                    # 公司简称变化
                    column = ('company_code', 'company_abbreviated')
                    data = (ret4[0], ret4[1])
                    new_data = (check_data[0], check_data[1])
                    change_company_name(spider.db, spider.cs, column, [data[0], data[1], new_data[1]])
                elif ret4 and ret4[2] != check_data[2]:
                    # a股简称变化
                    column = ('company_code', 'shares_name_A')
                    data = (ret4[0], ret4[2])
                    new_data = (check_data[0], check_data[2])
                    change_company_name(spider.db, spider.cs, column, [data[0], data[1], new_data[1]])
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
                    company_code, company_name_short, shares_code_B, shares_name_B, industry, company_detail_url,
                    '上交所',
                    get_time(), get_time())
                check_data = (company_code, company_name_short, shares_name_B)
                ret4 = [ret3[1], ret3[2], ret3[6]] if ret3 else None
                if ret4 and ret4[1] != check_data[1]:
                    # 公司简称变化
                    column = ('company_code', 'company_abbreviated')
                    data = (ret4[0], ret4[1])
                    new_data = (check_data[0], check_data[1])
                    change_company_name(spider.db, spider.cs, column, [data[0], data[1], new_data[1]])

                elif ret4 and ret4[2] != check_data[2]:
                    # b股简称变化
                    column = ('company_code', 'shares_name_B')
                    data = (ret4[0], ret4[2])
                    new_data = (check_data[0], check_data[2])
                    change_company_name(spider.db, spider.cs, column, [data[0], data[1], new_data[1]])
                # elif not ret4:
                #     # 新股上市
                #     update_data(spider.db,spider.cs,(('company_code','is_new'),(company_code,1)))
                params = (column, data)
            else:
                column = (
                    'company_code', 'company_abbreviated', 'shares_code_A', 'shares_name_A', 'shares_code_B',
                    'shares_name_B', 'industry',
                    'detail_url_in_exchange', 'exchange',
                    'create_time', 'update_time')
                data = (
                    company_code, company_name_short, shares_code_A, shares_name_A, shares_code_B, shares_name_B,
                    industry, company_detail_url,
                    '上交所',
                    get_time(), get_time())
                params = (column, data)
                # update_data(spider.db, spider.cs, params, SHARES_TABLE_NAME)
            if ret2:
                update_data(spider.db, spider.cs, params)
            else:
                # print('insert',"*"*100)
                # print(params)
                # print('insert', "-" * 100)
                ret = insert_data(spider.db, spider.cs, params, SHARES_TABLE_NAME)
                # print(ret)

        return item

    def open_spider(self, spider):
        '''开启爬虫执行一次'''
        if spider.name in ['sse_cp_notice', 'sse_shares']:
            pro_db, pro_cs = connect_mysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, PROXY_DB)

            spider.pro_db = pro_db
            spider.pro_cs = pro_cs
            ip_tuple = get_proxy(spider.pro_cs)
            spider.ip_tuple = ip_tuple
            # print(spider.ip_tuple)
        db, cs = connect_mysql(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE)
        # check_file.check_log('sse_notice.log')
        # check_file.check_log('sse_cp_notice.log')
        client = MongoClient(host='111.193.233.196', port=27017)
        coll = client.shangjiaosuo.sse
        data_cs = coll.find()
        coll_backup = client.shangjiaosuo.sse_backup
        spider.data_cs = data_cs
        spider.coll = coll
        spider.coll_backup = coll_backup
        spider.db = db
        spider.cs = cs

    def close_spider(self, spider):
        '''关闭爬虫执行一次'''
        spider.cs.close()
        spider.db.close()
        if spider.name in ['sse_cp_notice', 'sse_shares']:
            spider.pro_cs.close()
            spider.pro_db.close()
        spider.logger.info("当前为最后一次爬虫结束时间：%s" % time.ctime())


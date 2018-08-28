# -*- coding: utf-8 -*-
# -*- create by gt 18-8-14 -*-
from queue import Queue
from selenium import webdriver
import time
from lxml import etree
from pymysql import connect
from multiprocessing.dummy import Pool
import random
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from selenium.webdriver.common import proxy as ppppp


class WencaiSpider(object):
    def __init__(self):
        # self.queue = Queue()
        self.mongo = MongoClient(host='140.143.225.98', port=27017).wencai
        self.db = connect(host='10.10.0.11', port=3306, user='gaotao', password='124356', database='stockexchange',
                          charset='utf8')
        self.cs = self.db.cursor()
        self.proxy_db = connect(host='10.10.0.11', port=3306, user='gaotao', password='124356', database='callproxy',
                                charset='utf8')
        self.proxy_cs = self.proxy_db.cursor()
        self.basic_url = 'https://www.iwencai.com/stockpick/search?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w={}'
        self.pool = Pool(3)

    def get_shares_list(self):
        self.cs.execute('''select company_code from shares_list where shares_code_A is not null''')
        data_list = self.cs.fetchall()

        return [i[0] for i in data_list]

    def download(self, code, pro):

        option = webdriver.FirefoxOptions()
        pro_xy = ppppp.Proxy(
            raw={
                'proxyType': ppppp.ProxyType.MANUAL,
                'sslProxy': pro
            }
        )

        option.headless = True
        # profile.update_preferences()
        # profile.ssl_proxy = 'http://' + pro
        # pro_xy.ssl_proxy = 'http://' + pro
        # option.proxy = pro_xy
        # fireFoxOptions.proxy = 'http://{}'.format(pro_xy)
        browser = webdriver.Firefox(proxy=pro_xy, firefox_options=option)
        print(option.arguments)
        print(option.proxy)
        browser.get(self.basic_url.format(code))
        # time.sleep(7)
        page_source = browser.page_source
        browser.close()
        browser.quit()
        product, concept, flag = self.parse(page_source)
        if flag:
            self.save_page(code, page_source)

    def get_page(self):

        with open('wencai.txt', 'r') as f:
            while True:
                data = f.readline()
                if not data:
                    break
                data = json.loads(data)
                code = data['code']
                _id = data['_id']
                # print(_id)
                page = list(self.mongo.page.find({'_id': ObjectId(_id)}))
                page = page[0]['page']
                # page = list(db.test.find({'_id': ObjectId(_id)}))
                # print(page)
                # page = page[0]['page']
                yield code, page

    def parse(self, html_source):

        html = etree.HTML(html_source)
        product = html.xpath('//td[@colnum="4"]/div/span/a/text()')
        concept = html.xpath('//td[@colnum="5"]/div/span/a/text()')
        if product or concept:
            flag = True
        else:
            flag = False
        return product, concept, flag

    def pipeline(self, data_list):
        code, product, concept = data_list

        for pro in product:
            ret1 = self.check_db(pro, 'is_product=1', 1)
            if not ret1:
                pro_data = (0, pro, 1, None)
                pro_insert_sql = '''insert into `product&concept` value %s'''
                self.cs.execute(pro_insert_sql, [pro_data])
                self.db.commit()

            self.cs.execute('''select id from `product&concept` where name=%s''', [pro])
            pro_id = self.cs.fetchone()[0]
            insert_id = (0, code, pro_id)
            ret2 = self.check_db(pro, 'product_id={}'.format(pro_id), 2)
            if not ret2:
                pro_sql = '''insert into company_product value %s'''
                self.cs.execute(pro_sql, [insert_id])
                self.db.commit()
        for con in concept:
            ret1 = self.check_db(con, 'is_concept=1', 1)
            if not ret1:
                con_data = (0, con, None, 1)
                con_insert_sql = '''insert into `product&concept` value %s'''
                self.cs.execute(con_insert_sql, [con_data])
                self.db.commit()
            self.cs.execute('''select id from `product&concept` where name=%s''', [con])
            con_id = self.cs.fetchone()[0]
            insert_id1 = (0, code, con_id)
            ret2 = self.check_db(con, 'concept_id={}'.format(con_id), 2)
            if not ret2:
                con_sql = '''insert into company_concept value %s'''
                self.cs.execute(con_sql, [insert_id1])
                self.db.commit()

    def get_mongo(self):
        data = self.mongo.page.find({}, {'_id': 0, 'code': 1})
        return [i['code'] for i in data]

    def run(self):
        shares_list = self.get_shares_list()
        proxy_list = self.get_proxy()
        already_list = self.get_mongo()
        unfinished = set(shares_list) - set(already_list)
        # shares_list = ['000001', '000002', '000004', '000005']
        for code in unfinished:
            proxy = random.choice(proxy_list)
            print('download...')
            self.download(code, proxy)
            print('crawled:', self.basic_url.format(code))
            print(1)
            time.sleep(30)
            # print(code,proxy)
        self.pool.close()
        self.pool.join()
        # print(3)

    def check_db(self, name, flag, sql_id):
        if sql_id == 1:
            check_sql = '''select * from `product&concept` where name=%s and ''' + flag
        if sql_id == 2:
            check_sql = '''select * from `company_concept` where company_code=%s and ''' + flag
        if sql_id == 3:
            check_sql = '''select * from `company_product` where company_code=%s and ''' + flag
        ret = self.cs.execute(check_sql, [name])
        return ret

    def save(self):
        for code, page_source in self.get_page():
            # code, page_source = self.queue.get()
            product, concept, flag = self.parse(page_source)
            if not flag:
                with open('unfinished.txt', 'a+') as f:
                    f.write(code)
                    f.write('\r\n')
            self.pipeline([code, product, concept])

    def get_proxy(self):
        sql = '''select ip from `proxy`'''
        self.proxy_cs.execute(sql)
        proxy_list = self.proxy_cs.fetchall()
        return [proxy[0] for proxy in proxy_list]

    def save_page(self, code, page):
        _id = self.mongo.page.insert({'code': code, 'page': page})
        with open('wencai.txt', 'a+') as f:
            f.write(json.dumps({'_id': str(_id), 'code': code}))
            f.write('\r\n')

    def close(self):
        self.db.close()
        self.cs.close()
        self.proxy_db.close()
        self.proxy_cs.close()


if __name__ == '__main__':
    def download_save_page():
        spider = WencaiSpider()
        spider.run()
        spider.close()


    def parse_page():
        spider = WencaiSpider()
        spider.save()
        spider.close()


    download_save_page()
    # parse_page()

    # spider.run()
    # spider.save()
    # spider.close()
    print(4)

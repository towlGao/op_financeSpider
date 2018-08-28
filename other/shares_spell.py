# -*- coding: utf-8 -*-
# -*- create by gt 18-8-28 -*-
import requests
from lxml import etree
from multiprocessing.dummy import Pool
from pymysql import connect
import random
import time


class ShareSpellSpider(object):
    def __init__(self):
        self.pool = Pool(3)
        self.db = connect(host='10.10.0.11', port=3306, database='stockexchange', user='gaotao', password='124356',
                          charset='utf8')
        self.cs = self.db.cursor()
        self.pro_db = connect(host='10.10.0.11', port=3306, database='callproxy', user='gaotao', password='124356',
                              charset='utf8')
        self.pro_cs = self.pro_db.cursor()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.basic_url = 'http://www.yz21.org/stock/info/sz/{}/'
        self.ip_list = None
        self.shares_A_list = None
        self.shares_B_list = None
        self.shares_list = None

    def get_shares_list(self):
        self.cs.execute(
            '''select shares_code_A from shares_list where shares_code_A is not null''')
        shares_A_list = self.cs.fetchall()
        self.cs.execute(
            '''select shares_code_B from shares_list where shares_code_B is not null''')
        shares_B_list = self.cs.fetchall()
        shares_A_list = [share[0] for share in shares_A_list if share[0]]
        shares_B_list = [share[0] for share in shares_B_list if share[0]]
        self.shares_A_list = shares_A_list
        self.shares_B_list = shares_B_list

    def get_page(self, share):
        url = self.basic_url.format(share)
        print(time.ctime() + ',get_page:{}'.format(url))
        response = requests.get(url,
                                proxies={'http': 'http://{}'.format(random.choice(self.ip_list))})
        return response

    def save_data(self, data):
        print(time.ctime() + 'save...')
        share, spell = data
        if share in self.shares_A_list:
            sql = '''update shares_list set shares_spell_A=%s where shares_code_A=%s'''
        else:
            sql = '''update shares_list set shares_spell_B=%s where shares_code_B=%s'''
        self.cs.execute(sql, [spell, share])
        self.db.commit()

    def run(self):
        print(time.ctime() + '爬虫开启...')
        self.ip_list = self.get_proxy()
        self.get_shares_list()
        print(111)
        self.shares_list = self.shares_A_list + self.shares_B_list
        # self.shares_list = ['000001']
        for share in self.shares_list:
            print(share)
            response = self.get_page(share)
            spell = self.parse(response)

            self.save_data([share, spell])
        time.sleep(3)
        self.close()
        print(time.ctime() + '爬虫关闭...')

    def get_proxy(self):
        self.pro_cs.execute('''select ip from proxy''')
        ip_tuple = self.pro_cs.fetchall()
        return [ip[0] for ip in ip_tuple]

    def parse(self, response):
        html = etree.HTML(response.content.decode())
        spell = html.xpath('//table[@id="All_stocks1_DataGrid1"]//td[text()="拼音:"]/following-sibling::*[1]/text()')
        return spell[0].strip()

    def close(self):
        self.cs.close()
        self.db.close()
        self.pro_cs.close()
        self.pro_db.close()


if __name__ == '__main__':
    spider = ShareSpellSpider()
    spider.run()

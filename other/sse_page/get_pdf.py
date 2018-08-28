# -*- coding: utf-8 -*-
# -*- create by gt 18-8-23 -*-

import requests
from datetime import datetime, timedelta
import random
from pymongo import MongoClient
import time
from multiprocessing.dummy import Pool
from pymysql import connect
from queue import Queue
import json
import re


def retrying(retry_num):
    def retry(func):
        def inner(*args, **kwargs):
            for i in range(retry_num):
                try:
                    result = func(*args, **kwargs)
                    return result
                except:
                    pass
            with open('unfinished.txt','a+') as f:
                f.write(str(args))
                f.write('\r\n')
        return inner

    return retry


class SseSpider(object):
    max_retry = 3

    def __init__(self):
        self.concurr = 10
        self.pool = Pool(self.concurr)
        self.timeout = 30
        self._begin_time = datetime.strptime('2000-01-17', '%Y-%m-%d')
        self._end_time = datetime.strptime('2018-8-24', '%Y-%m-%d')
        self._month = timedelta(days=30)
        self.ip_list = self.get_proxy()
        self.proxies = {'http': 'http://{}'.format(random.choice(self.ip_list))}
        # self.mongo_host = '140.143.225.98'
        self.mongo_host = 'localhost'
        self.mongo_port = 27017
        self.client = self.conn_mongo(self.mongo_host, self.mongo_port)
        self.coll = self.client.shangjiaosuo.sse
        self.start_urls = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'

        self.queue = Queue()
        self.is_run = True
        self.headers = {
            'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
            'X-Requested-With': 'XMLHttpRequest',
            'Content - Type': 'application/json;charset=UTF-8',
            'User-Agent': self.get_ua()
        }
        self.basic_url = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?isPagination=true&productId=&keyWord=&reportType2=&reportType=ALL&beginDate={}&endDate={}&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo={}&pageHelp.beginPage={}&pageHelp.cacheSize=1&_={}'
        # jsonCallBack=jsonpCallback16530&

    def get_url(self):
        end_time = None
        while True:
            begin_time = end_time if end_time else self._begin_time
            if begin_time >= self._end_time:
                break
            end_time = begin_time + self._month
            beginTime = datetime.strftime(begin_time, '%Y-%m-%d')
            endTime = datetime.strftime(end_time, '%Y-%m-%d')
            url = self.basic_url.format(beginTime, endTime)
            self.queue.put(url)

    @retrying(retry_num=max_retry)
    def get_page(self, url):
        response = requests.get(url, timeout=self.timeout, headers=self.headers, proxies=self.proxies)
        return response

    def rand_float(self):
        rand_int = "0." + "".join([str(random.randint(0, 9)) for i in range(16)]) + str(random.randint(1, 9))
        return rand_int

    def get_time(self):
        tm = time.time() * 1000
        tm = int(tm)
        tm = str(tm)
        return tm[:13]

    def _request_save(self):
        url = self.queue.get()
        page_num = 1
        while True:
            url = url.format(page_num, self.get_time())
            end_time = re.findall(r'endDate=(\d+-\d+-\d+)', url)[0]
            response = self.get_page(url)
            json_data = json.loads(response.content.decode())
            result = json_data.get('result', [])
            if not result:
                if datetime.strptime(end_time, '%Y-%m-%d') >= self._end_time:
                    time.sleep(3)
                    self.is_run = False
                break
            page_num += 1
            self.save_json(json_data)

    def _callback(self, temp):
        if self.is_run:
            self.pool.apply_async(self._request_save, callback=self._callback)

    def run(self):
        print('爬虫开启...，'+str(datetime.now()))
        self.get_page(self.start_urls)
        for i in range(self.concurr):
            self.pool.apply_async(self._request_save, callback=self._callback)
        while True:
            time.sleep(0.0002)
            if not self.is_run:
                time.sleep(2)
                break
        self.client.close()
        print('爬虫结束...，' + str(datetime.now()))


    def get_proxy(self):
        pro_db = connect(host='140.143.225.98', port=3306, user='root', password='mysql', database='callproxy',
                         charset='utf8')
        pro_cs = pro_db.cursor()
        pro_cs.execute('''select ip from proxy''')
        ip_tuple = pro_cs.fetchall()
        pro_cs.close()
        pro_db.close()
        return [i[0] for i in ip_tuple]

    def get_ua(self):
        first_num = random.randint(55, 62)
        third_num = random.randint(0, 3200)
        fourth_num = random.randint(0, 140)
        os_type = [
            '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
            '(Macintosh; Intel Mac OS X 10_12_6)'
        ]
        chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

        ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                       '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                      )
        return ua

    def conn_mongo(self, host, port):
        client = MongoClient(host=host, port=port)
        return client

    def save_json(self, data):
        ret = {'data': data}
        self.coll.insert_one(ret)




# if __name__ == '__main__':
#
#     spider = SseSpider()
#     spider.run()

# coding=utf-8
import requests
from lxml import etree
import time
from queue import Queue
from multiprocessing.dummy import Pool

class QiuBai:
    def __init__(self):
        self.temp_url = "http://www.qiushibaike.com/8hr/page/{}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
        self.queue = Queue()
        self.pool= Pool(5)
        self.is_running = True
        self.total_request_num = 0
        self.total_response_num =0
        self.proxies = {"http":"http://192.126.158.36:80"}


    def get_url_list(self):
        for i in range(1,14):
            self.queue.put(self.temp_url.format(i))
            self.total_request_num += 1

    def parse_url(self,url):
        # response = requests.get(url,headers=self.headers,proxies=self.proxies)
        response = requests.get(url,headers=self.headers)
        print(response)
        return response.content.decode()

    def get_content_list(self,html_str):#提取数据
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[@id='content-left']/div")
        content_list = []
        for div in div_list:
            item = {}
            item["user_name"] = div.xpath(".//h2/text()")[0].strip()
            item["content"] = [i.strip() for i in div.xpath(".//div[@class='content']/span/text()")]
            content_list.append(item)
        return content_list

    def save_content_list(self,content_list): #保存
        for content in content_list:
            # print(content)
            pass

    def _execete_request_content_save(self):  #进行一次url地址的请求，提取，保存
        url = self.queue.get()
        html_str = self.parse_url(url)
        #3. 提取数据
        content_list = self.get_content_list(html_str)
        #4. 保存
        self.save_content_list(content_list)
        self.total_response_num +=1

    def _callback(self,temp):
        if self.is_running:
            self.pool.apply_async(self._execete_request_content_save,callback=self._callback)


    def run(self):#实现做主要逻辑
        #1. 准备url列表
        self.get_url_list()
        for i in range(3): #设置并发数为3
            self.pool.apply_async(self._execete_request_content_save,callback=self._callback)

        while True:
            time.sleep(0.0001)
            if self.total_response_num>= self.total_request_num:
                self.is_running = False
                break


if __name__ == '__main__':
    t1 = time.time()
    qiubai = QiuBai()
    qiubai.run()
    print("total cost:",time.time()-t1)
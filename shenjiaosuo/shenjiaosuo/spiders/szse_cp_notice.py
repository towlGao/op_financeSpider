# -*- coding: utf-8 -*-
import scrapy
import random
import re
import json
import w3lib.url
from pprint import pprint
from hashlib import sha1
from copy import deepcopy
from shenjiaosuo.items import ShenjiaosuoItemCp
from shenjiaosuo.settings import APPENDIX_DIR, UPDATE_FLAG, NOTICE_UPDATE_NUM
import time
from utils import check_file
from datetime import datetime, timedelta


def rand_float():
    rand_int = "0." + "".join([str(random.randint(0, 9)) for i in range(16)]) + str(random.randint(1, 9))

    return rand_int


class SzseSpider(scrapy.Spider):
    name = 'szse_cp_notice'
    allowed_domains = []
    default_pagesize = 30
    default_page = 1
    lpage_url = 'http://www.szse.cn/api/disc/announcement/annList?random={}'
    start_urls = [
        'http://www.szse.cn/api/disc/announcement/searchQuery?random={}&annType=szse'.format(rand_float())]
    appendix_dir = check_file.appendix_dir if check_file.appendix_dir else check_file.check_app_dir()

    # start_urls = [
    #     'http://www.szse.cn/api/disc/announcement/detailinfo?random={}&pageSize={}&pageNum={}&plateCode=szse'.format(
    #         rand_float(), default_pagesize, default_page)]


    def parse(self, response):
        '''获取分类信息'''
        json_data = json.loads(response.body.decode())
        category_info = json_data.get("categoryInfo")
        for i in category_info:
            category_id = i.get("value")
            category_name = i.get("text")
            list_page_url = SzseSpider.lpage_url.format(rand_float())
            formdata = {
                "seDate": ["", ""],
                "channelCode": ["listedNotice_disc"],
                "bigCategoryId": [str(category_id)],
                "pageSize": 30,
                "pageNum": 1,
                "sortPublishTime": "asc"
            }

            yield scrapy.Request(
                url=list_page_url,
                method="POST",
                body=json.dumps(formdata),
                meta={'category_name': category_name, 'category_id': category_id},
                callback=self.parse_paging
            )

    def parse_paging(self, response):
        '''分类解析函数'''
        category_id = response.meta.get("category_id")
        category_name = response.meta.get("category_name")
        json_data = json.loads(response.body.decode())
        data = json_data.get('data')
        ear_time = data[0].get('publishTime').split(" ")[0]
        ear_time = datetime.strptime(ear_time, "%Y-%m-%d")
        now_time = datetime.now()
        month_ = timedelta(days=30)
        update = timedelta(days=NOTICE_UPDATE_NUM)
        count = (now_time - ear_time) // month_ + 1

        list_page_url = SzseSpider.lpage_url.format(rand_float())
        # 页数最大500，按日期进行爬取
        if UPDATE_FLAG is True:
            start_time = datetime.now()
            end_time = start_time - update
            s_time = datetime.strftime(start_time, "%Y-%m-%d")
            e_time = datetime.strftime(end_time, "%Y-%m-%d")

            formdata = {
                "seDate": [s_time, e_time],
                "channelCode": ["listedNotice_disc"],
                "bigCategoryId": [str(category_id)],
                "pageSize": 30,
                "pageNum": 1
            }
            item = ShenjiaosuoItemCp()
            item['category'] = category_name
            # time.sleep(0.2)
            yield scrapy.Request(
                url=list_page_url,
                method='POST',
                body=json.dumps(formdata),
                meta={"item": deepcopy(item), 'category_id': category_id, 'data': formdata, "seDate": [s_time, e_time]},
                callback=self.parse_t_lpage
            )
        else:
            start_time = ear_time
            end_time = ear_time + month_

            for time_num in range(count):
                s_time = datetime.strftime(start_time, "%Y-%m-%d")
                e_time = datetime.strftime(end_time, "%Y-%m-%d")

                formdata = {
                    "seDate": [s_time, e_time],
                    "channelCode": ["listedNotice_disc"],
                    "bigCategoryId": [str(category_id)],
                    "pageSize": 30,
                    "pageNum": 1
                }
                self.logger.info(formdata)
                item = ShenjiaosuoItemCp()
                item['category'] = category_name
                # time.sleep(0.2)
                yield scrapy.Request(
                    url=list_page_url,
                    method='POST',
                    body=json.dumps(formdata),
                    meta={"item": deepcopy(item), 'category_id': category_id, 'data': formdata,
                          "seDate": [s_time, e_time]},
                    callback=self.parse_t_lpage
                )
                start_time = end_time
                end_time += month_
                if start_time > datetime.now():
                    return

    def parse_t_lpage(self, response):
        '''根据时间访问的列表页信息'''
        item = response.meta.get("item")
        category_id = response.meta.get("category_id")

        json_data = json.loads(response.body.decode())
        s_time = response.meta.get("seDate")[0]
        e_time = response.meta.get("seDate")[1]
        ann_count = json_data.get("announceCount")
        # print(ann_count)
        data = json_data.get("data")
        if data == "{}":
            return
        total_page = int(ann_count) // 30 + 1
        for page_num in range(total_page):
            formdata = {
                "seDate": [s_time, e_time],
                "channelCode": ["listedNotice_disc"],
                "bigCategoryId": [str(category_id)],
                "pageSize": 30,
                "pageNum": page_num + 1
            }
            list_page_url = SzseSpider.lpage_url.format(rand_float())
            self.logger.info(formdata)
            # item = ShenjiaosuoItemCp()
            # item['category'] = category_name
            # time.sleep(0.2)
            yield scrapy.Request(
                url=list_page_url,
                method='POST',
                body=json.dumps(formdata),
                meta={"item": deepcopy(item), 'data': formdata, "seDate": [s_time, e_time]},
                callback=self.parse_lpage
            )

    def parse_lpage(self, response):
        '''列表页解析函数'''
        item = response.meta.get("item")
        json_data = json.loads(response.body.decode())
        data = json_data.get('data')

        # pprint(response.body.decode())
        # print(response.meta['data'])
        # print(response.meta['total'])
        for i in data:

            item['l1_title'] = '上市公司信息'
            item['l2_title'] = '上市公司公告'
            item['detail_url'] = i.get("attachPath")
            item['publish_time'] = i.get("publishTime")
            item['publish_time'] = item['publish_time'].rsplit(' ', 1)[0]
            item['sec_code'] = i.get("secCode")[0]
            item['sec_name'] = i.get("secName")[0]
            item['title'] = i.get("title")
            item['doc_type'] = i.get("attachFormat")
            item['content'] = None
            if item['doc_type'].lower() == 'html':
                '''html文件内容提取'''

                item['appendix_path'] = None
                detail_url = "http://www.szse.cn" + item['detail_url']
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.detail_parse,
                    meta={'item': deepcopy(item)}
                )
            else:

                item['appendix_path'] = []
                if isinstance(item['detail_url'], str):
                    appendix_url_list = [item['detail_url']]
                else:
                    appendix_url_list = item['detail_url']
                for appendix_url in appendix_url_list:
                    appendix_url = w3lib.url.canonicalize_url(appendix_url)
                    s1 = sha1()
                    appendix_url = "http://disc.static.szse.cn" + appendix_url
                    item['detail_url'] = appendix_url
                    s1.update(appendix_url.encode())
                    fp1 = s1.hexdigest()
                    type = item['doc_type']
                    if type in ['cn', 'com']:
                        item['appendix_path'] = None
                        yield item
                    else:
                        SzseSpider.appendix_dir = check_file.check_app_dir()
                        item['appendix_path'].append(SzseSpider.appendix_dir + fp1 + '.' + type)
                        # print(item['appendix_path_list'],item['detail_url'],appendix_url)
                        start_time = time.time()
                        yield scrapy.Request(
                            appendix_url,
                            meta={'item': deepcopy(item), 'fp1': fp1, 'start_time': start_time},

                            callback=self.appendix_parse
                        )

    def appendix_parse(self, response):
        '''pdf下载'''
        end_time = time.time()
        start_time = response.meta['start_time']
        time_ = end_time - start_time
        fp1 = response.meta['fp1']
        item = response.meta['item']
        type = item['doc_type']
        start_time2 = time.time()
        with open(SzseSpider.appendix_dir + fp1 + '.' + type, 'wb') as f:
            f.write(response.body)
        # print(item)
        end_time2 = time.time()
        time2_ = end_time2 - start_time2
        if time2_ > time_:
            self.logger.info('time1:{},time2:{}'.format(time_,time2_))
        item['handle_time'] = [time_,time2_]
        yield item

    def detail_parse(self, response):
        '''html详情页解析函数'''
        item = response.meta.get('item')
        span_list = response.xpath("//hr/following-sibling::*[1]//span")
        if not span_list:
            span_list = response.xpath("//span[@class='da']")
        content_span = span_list[-1]
        content = content_span.xpath(".//text()").extract()
        content = [i.strip() for i in content if i.strip()]
        ret = re.findall(r"\w+?年\w+?月\w+?日", content[-1])
        if ret:
            content.pop()

        item['content'] = content
        # print(item)

        yield item

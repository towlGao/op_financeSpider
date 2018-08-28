# # -*- coding: utf-8 -*-
# import scrapy
# import time
# import re
# import json
# from datetime import datetime, timedelta
# from copy import deepcopy
# import random
# from hashlib import sha1
# import w3lib.url
# from utils import check_file
# from shangjiaosuo.settings import APPENDIX_DIR, UPDATE_FLAG, NOTICE_UPDATE_NUM
#
#
# # from pprint import pprint
# def get_time():
#     tm = time.time() * 1000
#     tm = int(tm)
#     tm = str(tm)
#     return tm[:13]
#
#
# def get_random():
#     num = str(random.random())
#     num = num.replace('.', '')
#     num = int(num)
#     return str(num)[:5]
#
#
# class SseCpNoticeSpider(scrapy.Spider):
#     name = 'sse_cp_notice'
#     allowed_domains = ['sse.com.cn']
#     begin_time = datetime.strftime(datetime.now(), '%Y-%m-%d').split(" ")[0]
#     appendix_dir = check_file.appendix_dir if check_file.appendix_dir else check_file.check_app_dir()
#
#     # start_urls = ['http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?jsonCallBack=jsonpCallback10000&isPagination=true&productId=&keyWord=&reportType2=&reportType=ALL&beginDate={}&endDate={}&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_={}'.format(begin_time,begin_time,int(time.time()*1000))]
#
#     def start_requests(self):
#         start_url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm'
#         headers = {
#             'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
#             'X-Requested-With': 'XMLHttpRequest'
#         }
#         yield scrapy.Request(url=start_url, method='POST', headers=headers, dont_filter=True, callback=self.parse)
#
#     def parse(self, response):
#         '''获取最近书据从而获取开始时间,再跟据分类访问'''
#         dd_list = response.xpath("//dl[@class='modal_pdf_list']/dd")
#         end_time = dd_list[0].xpath('./@data-time').extract_first().strip().split(' ')[0]
#         month_ = timedelta(days=30)
#         endTime = datetime.strptime(end_time, "%Y-%m-%d")
#         end_time = datetime.strftime(endTime, "%Y-%m-%d")
#         beginTime = endTime - month_
#         begin_time = datetime.strftime(beginTime, "%Y-%m-%d")
#         option_str = '''<option value="YEARLY" >  年报</option><option value="QUATER1" >  第一季度季报</option><option value="QUATER2" >  半年报</option><option value="QUATER3" >  第三季度季报</option>' +
# 			'<option value="SHGSZC" >  上市公司章程</option><option value="FXSSGG" >  发行上市公告</option><option value="GSZL" >  公司治理</option><option value="GDDH" >  股东大会会议资料</option>' +
# 			'<option value="IPOGG" >  IPO公司公告</option><option value="QT" >  其他</option>'''
#         option_list = re.findall(r'<option value="([A-Z]+?\d*?)".*?>(.+?)</option>', option_str)
#         category_type = ['定期公告', '临时公告']
#         for category in option_list:  # todo:
#             item = {}
#             item['category_value'] = category[0]
#             item['category_name'] = category[1].strip()
#             if item['category_name'] in ['年报', '第一季度季报', '半年报', '第三季度季报']:
#                 item['category_name'] = '定期公告-' + item['category_name']
#                 item['category_value1'] = 'DQGG'
#             elif item['category_name'] in ['上市公司章程', '发行上市公告', '公司治理', '股东大会会议资料', 'IPO公司公告', '其他']:
#                 item['category_name'] = '临时公告-' + item['category_name']
#                 item['category_value1'] = 'LSGG'
#             tpage_url = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?isPagination=true&productId=&keyWord=&reportType2={}&reportType={}&beginDate={}&endDate={}&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&_={}'.format(
#                 item['category_value1'], item['category_value'], begin_time, end_time,
#                 get_time())
#             # pprint(item)
#             yield scrapy.Request(
#                 url=tpage_url,
#                 meta={'end_time': end_time, 'item': deepcopy(item)},
#                 callback=self.tpage_parse,
#                 dont_filter=True
#             )
#
#     def tpage_parse(self, response):
#         '''分时间段访问'''
#         # month_ = response.meta['month_']
#         item = response.meta['item']
#         # json_data = json.loads(re.findall(r'jsonpCallback\d+\((.*)\)', response.body.decode())[0])
#         json_data = json.loads(response.body.decode())
#         page_help = json_data['pageHelp']
#         data = page_help['data']
#         end_time = response.meta['end_time']
#         history_end_time = '2000-01-01'
#         history_end_time = datetime.strptime(history_end_time, "%Y-%m-%d")
#         endTime = datetime.strptime(end_time, "%Y-%m-%d")
#         if UPDATE_FLAG is True:
#             update = timedelta(days=NOTICE_UPDATE_NUM)
#             start_time = datetime.now()
#             end_time = start_time - update
#             startTime = datetime.strftime(start_time, '%Y-%m-%d')
#             endTime = datetime.strftime(end_time, '%Y-%m-%d')
#             lpage_url = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?isPagination=true&productId=&keyWord=&reportType2={}&reportType={}&beginDate={}&endDate={}&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&_={}'.format(
#                 item['category_value1'], item['category_value'], endTime, startTime,
#                 get_time())
#             yield scrapy.Request(
#                 url=lpage_url,
#                 meta={'end_time': endTime, 'item': deepcopy(item)},
#                 callback=self.lpage_parse,
#                 dont_filter=True
#             )
#         else:
#             while True:
#
#                 if endTime < history_end_time:
#                     return
#                 # page_count = page_help['pageCount']
#
#                 month_ = timedelta(days=30)
#                 endTime = datetime.strptime(end_time, "%Y-%m-%d")
#                 beginTime = endTime - month_
#                 begin_time = datetime.strftime(beginTime, "%Y-%m-%d")
#                 lpage_url = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?isPagination=true&productId=&keyWord=&reportType2={}&reportType={}&beginDate={}&endDate={}&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&_={}'.format(
#                     item['category_value1'], item['category_value'], begin_time, end_time,
#                     get_time())
#
#                 yield scrapy.Request(
#                     url=lpage_url,
#                     meta={'end_time': end_time, 'item': deepcopy(item)},
#                     callback=self.lpage_parse,
#                     dont_filter=True
#                 )
#                 end_time = begin_time
#                 # print(begin_time,end_time,"*"*100)
#
#     def lpage_parse(self, response):
#         '''翻页'''
#         item = response.meta['item']
#         # json_data = json.loads(re.findall(r'jsonpCallback\d+\((.*)\)', response.body.decode())[0])
#         json_data = json.loads(response.body.decode())
#         page_help = json_data['pageHelp']
#         data = page_help['data']
#         page_count = page_help['pageCount']
#         # 翻页
#         for page in range(int(page_count)):
#             # for page_num in range(1):
#             page_num = page + 1
#             url = re.sub(r'pageHelp\.pageNo=\d+', 'pageHelp.pageNo={}'.format(page_num), response.url)
#             url = re.sub(r'_=\d+', '_={}'.format(get_time()), url)
#             # url = re.sub(r'jsonCallBack=jsonpCallback\d+',
#             #              'jsonCallBack=jsonpCallback{}'.format(get_random()), url)
#             # print(re.findall(r'pageHelp\.pageNo=(\d+)', url)[0][0])
#             yield scrapy.Request(
#                 url=url,
#                 meta={'item': deepcopy(item)},
#                 callback=self.list_page_parse,
#                 dont_filter=True
#             )
#
#     def list_page_parse(self, response):
#         item = response.meta['item']
#         # json_data = json.loads(re.findall(r'jsonpCallback\d+\((.*)\)', response.body.decode())[0])
#         json_data = json.loads(response.body.decode())
#         data = json_data['result']
#         if not data:
#             self.logger.error('没有data',response.body.decode())
#         for i in data:
#             item['l1_title'] = '上市公司信息'
#             item['l2_title'] = '最新公告'
#             item['title'] = i['title']
#             item['sec_code'] = i['security_Code']
#             item['sec_name'] = None
#             item['appendix_path_list'] = []
#             item['publish_time'] = i['SSEDate']
#             item['detail_url'] = i['URL']
#             item['doc_type'] = item['detail_url'].rsplit('.', 1)[1]
#             item['content'] = None
#
#             if item['doc_type'].lower() in ['pdf', 'doc', 'docx']:
#                 url = 'http://static.sse.com.cn' + item['detail_url']
#             else:
#                 url = 'http://www.sse.com.cn' + item['detail_url']
#                 self.logger.info('*' * 100)
#             yield scrapy.Request(
#                 url=url,
#                 meta={'item': deepcopy(item)},
#                 callback=self.detail_parse
#             )
#
#     def detail_parse(self, response):
#         '''详情页'''
#         SseCpNoticeSpider.appendix_dir = check_file.check_app_dir()
#         item = response.meta['item']
#         s = sha1()
#         url = w3lib.url.canonicalize_url(response.url)
#         s.update(url.encode())
#         fp1 = s.hexdigest()
#         with open(SseCpNoticeSpider.appendix_dir + fp1 + '.' + item['doc_type'], 'wb') as f:
#             f.write(response.body)
#             item['appendix_path_list'].append(SseCpNoticeSpider.appendix_dir + fp1 + '.' + item['doc_type'])
#         # print(item)
#         yield item
# -*- coding: utf-8 -*-
import scrapy
import time
import re
from bson import ObjectId
import json
from datetime import datetime, timedelta
from copy import deepcopy
import random
from hashlib import sha1
import w3lib.url
from utils import check_file
from shangjiaosuo.settings import APPENDIX_DIR, UPDATE_FLAG, NOTICE_UPDATE_NUM


# from pprint import pprint
def get_time():
    tm = time.time() * 1000
    tm = int(tm)
    tm = str(tm)
    return tm[:13]


def get_random():
    num = str(random.random())
    num = num.replace('.', '')
    num = int(num)
    return str(num)[:5]


class SseCpNoticeSpider(scrapy.Spider):
    name = 'sse_cp_notice'
    allowed_domains = []
    # begin_time = datetime.strftime(datetime.now(), '%Y-%m-%d').split(" ")[0]
    appendix_dir = check_file.appendix_dir if check_file.appendix_dir else check_file.check_app_dir()

    start_urls = ['http://www.sse.com.cn/disclosure/listedinfo/announcement/']

    # def start_requests(self):
    #     start_url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm'
    #     headers = {
    #         'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
    #         'X-Requested-With': 'XMLHttpRequest'
    #     }
    #     yield scrapy.Request(url=start_url, method='POST', headers=headers, dont_filter=True, callback=self.parse)

    def parse(self, response):
        for data in self.data_cs:
            try:
                json_data = json.loads(data['data'])
            except:
                with open('unfinished.txt', 'a+') as f:
                    f.write(str({'url': response.url, 'content': response.body.decode()}))
                    f.write('\r\n')
            _id = data['_id']
            if not json_data['result']:
                continue
            for eve_data in json_data['result']:
                item = {}
                item['l1_title'] = '上市公司信息'
                item['l2_title'] = '最新公告'
                item['category'] = eve_data['bulletin_Type']
                item['title'] = eve_data['title']
                item['sec_code'] = eve_data['security_Code']
                item['sec_name'] = None
                item['detail_url'] = 'http://static.sse.com.cn' + eve_data['URL']
                item['doc_type'] = item['detail_url'].rsplit('.', 1)[1]
                item['publish_time'] = eve_data['SSEDate']
                item['appendix_path_list'] = []
                item['content'] = None
                yield scrapy.Request(item['detail_url'], meta={'item': item, '_id': _id}, callback=self.detail_parse)

    def detail_parse(self, response):
        '''下载pdf'''
        item = response.meta['item']
        SseCpNoticeSpider.appendix_dir = check_file.check_app_dir()
        _id = response.meta['_id']
        s = sha1()
        url = w3lib.url.canonicalize_url(response.url)
        s.update(url.encode())
        fp1 = s.hexdigest()
        try:
            with open(SseCpNoticeSpider.appendix_dir + fp1 + '.' + item['doc_type'], 'wb') as f:
                f.write(response.body)
                item['appendix_path_list'].append(SseCpNoticeSpider.appendix_dir + fp1 + '.' + item['doc_type'])
            # print(item)
            self.coll.remove({'_id':ObjectId(_id)})
            yield item
        except:
            with open('unfinished2.txt','a+') as f:
                f.write(str({'url':response.url,'item':item}))
                f.write('\r\n')

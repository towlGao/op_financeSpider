# -*- coding: utf-8 -*-
# -*- create by gt 18-7-23 -*-
# import json
# import re
# # a = ['abc','sdf','spe','fgr']
# #
# # b = json.dumps(a)
# # print(b)
# # print(type(b))
# #
# # c = json.loads(b)
# # print(c)
# # print(type(c))
import requests

# url = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?jsonCallBack=jsonpCallback60838&isPagination=true&productId=&keyWord=&reportType2=&reportType=ALL&beginDate=2018-06-25&endDate=2018-07-25&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1532487769876'
# url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/s_docdatesort_desc_2016openpdf.htm'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    # 'Cookie': 'yfx_c_g_u_id_10000042=_ck18072510500811360687535714231; VISITED_MENU=%5B%228349%22%5D; yfx_f_l_v_t_10000042=f_t_1532487008113__r_t_1532487008113__v_t_1532487769489__r_c_0',
    # 'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'
}

# response = requests.post(url,headers=headers)
#
#
# resp = response.content.decode()
# json_data = re.findall(r'jsonpCallback(\d+?)\((.*)\)',resp)
# # print(json_data)
# # count = json_data[0]
# print(resp)
# json_data = count[1]
# count = count[0]
# jsondata = json.loads(json_data)
# print(count)
# print(jsondata['result'])
# print(len(jsondata['result']))

# option_str = '''<option value="DQGG">定期公告</option><option value="YEARLY" >  年报</option><option value="QUATER1" >  第一季度季报</option><option value="QUATER2" >  半年报</option><option value="QUATER3" >  第三季度季报</option>' +
# 			'<option value="LSGG">临时公告</option><option value="SHGSZC" >  上市公司章程</option><option value="FXSSGG" >  发行上市公告</option><option value="GSZL" >  公司治理</option><option value="GDDH" >  股东大会会议资料</option>' +
# 			'<option value="IPOGG" >  IPO公司公告</option><option value="QT" >  其他</option>'''
# option_list = re.findall(r'<option value="([A-Z]+?)".*?>(.+?)</option>',option_str)
# for category in option_list:
#     item = {}
#     item['category_value'] = category[0]
#     item['category_name'] = category[1].strip()
#     print(item)
# import random
#
# print(random.random())
# import random
# import time
# from datetime import datetime,timedelta
# # # a = 'asdfew{}'.format(3)
# # # print(a)
# tpage_url = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?jsonCallBack=jsonpCallback{}&isPagination=true&productId=&keyWord=&reportType2={}&reportType=ALL&beginDate={}&endDate={}&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_={}'.format(
#     int(random.random() * (100000 + 1)), 'DQGG', '2018-3-3', '2018-2-1', int(time.time() * 1000))
#
# print(tpage_url)
# end_time = '2018-7-25'
# month_ = timedelta(days=30)
# endTime = datetime.strptime(end_time, "%Y-%m-%d")
# beginTime = endTime - month_
# begin_time = datetime.strftime(beginTime, "%Y-%m-%d")
# end_time = datetime.strftime(endTime,"%Y-%m-%d")
# print(begin_time,end_time)
import json
from hashlib import sha1
from lxml import etree
# from pymysql import connect
# db = connect(host='10.10.0.11', port=3306, user='gaotao', password='124356',
#              # database='callproxy',
#              database='stockexchange',
#                  charset="utf8")
# cs = db.cursor()
#
# # sql ='''select ip from proxy'''
# sql ='''select id,detail_url from exchange_notice where l1_title='上交所公告' and appendix_pathList is not null'''
# ret = cs.execute(sql)
#
# data1 = cs.fetchall()
# print(data1)
# total = 0
# for tup in data1:
#     id = tup[0]
#     detail_url = tup[1]
#     if detail_url.startswith('/'):
#         detail_url = 'http://www.sse.com.cn' + detail_url
#     resp = requests.get(detail_url,headers=headers)
#     html = etree.HTML(resp.content)
#     app_list = html.xpath("//div[@class='allZoom']//a/@href")
#     # print(app_list)
#     app_list = [url for url in app_list if url.rsplit('.',1)[1].lower() in ['docx','doc','pdf']]
    # print(app_list)
#     app_list = app_list if app_list else None
#     app_list2 = []
#     if app_list:
#         # total += len(app_list)
#         for app_url in app_list:
#             app_url = 'http://www.sse.com.cn' + app_url
#             s1 = sha1()
#             s1.update(app_url.encode())
#             fp = s1.hexdigest()
#             app_list2.append('/data/gaotao/stockex_change/exchange_file/02/'+fp+'.'+app_url.rsplit('.',1)[1])
#             response = requests.get(app_url,headers=headers)
#             with open('/data/gaotao/stockex_change/exchange_file/02/'+fp+'.'+app_url.rsplit('.',1)[1],'wb') as f:
#                 f.write(response.content)
#     app_list2 = app_list2 if app_list2 else None
#     json_str = json.dumps(app_list2)
#     data = (json_str,id)
#     print(type(data[0]),type(data[1]))
#     print(app_list2)
#     update_sql = '''update exchange_notice set appendix_pathList=%s where id=%s'''
#     print(update_sql)
#     result = cs.execute(update_sql,[data[0],data[1]])
#     db.commit()
# cs.close()
# db.close()

# print(total)
# print(len(data))
# print(type(data))
# print(json.loads(data[0]))
# import requests
# for ip in data:
#
#     proxies = {"http": "http://{}".format(ip[0])}
#     try:
#         requests.get("https://www.google.com.hk/", proxies=proxies)
#         print("连接成功",ip[0])
#     except:
#         print('链接失败')



# import requests
#
#
# url = 'http://news.yule.com.cn/neidi/'
#
# # headers={
# #     'User-Agent':
# # }
# response = requests.get(
#
#     url=url,
#     headers=headers
# )
#
# from lxml import etree
#
#
# html = etree.HTML(response.content)
#
# li_list = html.xpath('//div[@class="MBL"]/ul/li')
#
# for li in li_list:
#     title = li.xpath(".//div[@class='titname']/a/text()")[0].strip()
#     href = li.xpath(".//div[@class='titname']/a/@href")
#     print(title, href)
url2 = ' http://www.szse.cn/api/disc/announcement/annList?random=0.12127292001259261'
resp = requests.post(url2,headers=headers)
print(resp.content.decode())





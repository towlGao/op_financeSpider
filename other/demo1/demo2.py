# -*- coding: utf-8 -*-
# -*- create by gt 18-8-27 -*-
import requests
import re
from pymongo import MongoClient

client = MongoClient(host='111.193.233.196',port=27017)
coll = client.shangjiaosuo.sse
with open('unfinished.txt', 'r+') as f:
    content = f.readlines()
    # print(content)
# content.pop(0)
# content.pop(0)

headers = {
            'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
for i in content:
    url = i.split(',')[1][2:-3]
    response = requests.get(url,headers=headers)
    print({'data':response.content.decode()})
    coll.insert({'data':response.content.decode()})
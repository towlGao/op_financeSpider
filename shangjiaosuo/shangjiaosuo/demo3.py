# -*- coding: utf-8 -*-
# -*- create by gt 18-8-27 -*-
from pymongo import MongoClient
# from pymongo import
from bson import ObjectId
import time
import json


client = MongoClient(host='111.193.233.196',port=27017)

old_coll = client.shangjiaosuo.sse
# new_coll = client.shangjiaosuo.sse_backup
coll2 = client.shangjiaosuo.text
# for i in old_coll.find():
#     time.sleep(0.0001)
    # new_coll.insert(i)
data = old_coll.find_one()
data2 = old_coll.find_one()
print(data)
print(data['_id'])
# coll2.insert(data)
# coll2.insert({'data':'hello'})
# print(len(list(coll2.find())))
# coll2.remove({'_id':ObjectId(data['_id'])})
# print(len(list(coll2.find())))
data3 = list(coll2.find())[2]
content = json.loads(data3['data'])
print(len(content['result']))
print(content['pageHelp']['data'][0])
for con in content['result']:
    print(con)


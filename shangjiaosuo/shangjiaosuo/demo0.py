# -*- coding: utf-8 -*-
# -*- create by gt 18-7-26 -*-

# import time
# from utils import check_file
# import os
#
# app_dir = check_file.appendix_dir if check_file.appendix_dir else check_file.check_app_dir()
#
# for i in range(101):
#     with open(os.path.join(app_dir,'{}.txt'.format(i)),'w') as f:
#         pass
#     app_dir = check_file.check_app_dir()
#
# print(app_dir)
# for i in range(100):
#     f1 = open('../sse_notice.log', 'a+')
#     f2 = open('../sse_cp_notice.log', 'a+')
#     time.sleep(0.05)
#     f1.write('*'*5)
#     f2.write('*'*4)
#     f1.close()
#     f2.close()
#     time.sleep(0.05)
#     check_file.check_log('sse_notice.log')
#     check_file.check_log('sse_cp_notice.log')

# with open('1.txt', 'w') as f:
#     for i in range(30):
#         f.write("*"*5*i)
#         f.write('\r\n')

# with open('1.txt', 'r') as f:
#     while True:
#         content = f.readline()
#         if not content:
#             break
#         print(content)
# for i in range(100):
#     f1 = open('1.txt','a')
#     f1.write('*'*10)
#     f1.close()
#     size = os.path.getsize('1.txt')
#     print(size)




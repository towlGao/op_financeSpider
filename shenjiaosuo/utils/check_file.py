# -*- coding: utf-8 -*-
# -*- create by gt 18-7-26 -*-
from shenjiaosuo.settings import APPENDIX_DIR, LOG_SIZE, APP_DIR_SIZE
import os
import re

szse_log_index = 0
szse_cp_log_index = 0
appendix_dir = None


def check_log(log_name):
    '''检查log日志文件，如果大于一定大小则重新生成一个日志文件'''
    global szse_log_index, szse_cp_log_index
    this_path = os.getcwd()
    #this_dir = this_path.rsplit('/', 1)[0]
    this_dir = this_path
    log_file = os.path.join(this_dir, log_name)
    log_file_size = os.path.getsize(log_file)
    if log_file_size >= LOG_SIZE:
        if log_name == 'szse_notice.log':
            new_log_name = log_name.split('.')[0] + str(szse_log_index) + '.' + log_name.split('.')[1]
            szse_log_index += 1
        if log_name == 'szse_cp_notice.log':
            new_log_name = log_name.split('.')[0] + str(szse_cp_log_index) + '.' + log_name.split('.')[1]
            szse_cp_log_index += 1
        log_dir = os.path.join(this_dir, 'spider_logs')
        with open(os.path.join(this_dir, log_name), 'r') as f1:
            with open(os.path.join(log_dir, new_log_name), 'w') as f:
                while True:
                    content = f1.readline()
                    if not content:
                        break
                    f.write(content)
                with open(os.path.join(this_dir, log_name), 'w') as f2:
                    pass

def check_app_dir():
    global appendix_dir
    appendix_dir = appendix_dir if appendix_dir else APPENDIX_DIR
    list_dir = os.listdir(appendix_dir)
    print(len(list_dir))
    if len(list_dir) >= APP_DIR_SIZE:
        dir_index = re.findall(r'\d+', appendix_dir)[0]
        new_dir_index = int(dir_index)+ 4
        appendix_dir = re.sub(r'\d+', str(new_dir_index), appendix_dir)
        if not os.path.exists(appendix_dir):
            os.mkdir(appendix_dir)
    return appendix_dir

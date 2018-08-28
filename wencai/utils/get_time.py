# -*- coding: utf-8 -*-
# -*- create by gt 18-7-26 -*-
import time


def get_time():
    local_time = time.localtime(time.time())
    curr_time = "%d-%02d-%02d %02d:%02d:%02d" % (
        local_time.tm_year, local_time.tm_mon, local_time.tm_mday, local_time.tm_hour, local_time.tm_min,
        local_time.tm_sec)
    return curr_time
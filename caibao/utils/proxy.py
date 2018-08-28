# -*- coding: utf-8 -*-
# -*- create by gt 18-8-8 -*-
from pymysql import connect
import requests


def get_proxy(cs):

    ret = cs.execute('''select ip from proxy''')
    ip_tuple = cs.fetchall()
    return [ip[0] for ip in ip_tuple]




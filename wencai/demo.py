# # -*- coding: utf-8 -*-
# # -*- create by gt 18-8-13 -*-
#

import execjs


def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("2.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    f.close()
    return htmlstr


jsstr = get_js()
ctx = execjs.compile(jsstr)
print(ctx.call('hello'))
# v='AjMBrqG6bKg7GiB8md8ZrWMWwjxeaMcqgfwLXuXQj9KJ5F0qbThXepHMm6z2'
# print(len(v))
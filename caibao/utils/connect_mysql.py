# -*- coding: utf-8 -*-
# -*- create by gt 18-7-26 -*-
from pymysql import connect
from datetime import datetime
from collections import Counter


def connect_mysql(host, port, user, passwd, database):
    db = connect(host=host, port=port, user=user, password=passwd, database=database,
                 charset="utf8")
    cs = db.cursor()

    return db, cs


def insert_data(db, cs, data, table):
    # if table == 'finance_info':
    insert_sql = 'insert into finance_info value %s'
    ret = cs.execute(insert_sql, [data])
    db.commit()
    print('1'*50)
    return ret
    # elif table == 'company_notice':
    #     insert_sql = 'insert into company_notice value %s'
    #     ret = cs.execute(insert_sql, data)
    #     db.commit()
    #     print('1'*50)
    #     return ret
    # elif table == 'shares_list':
    #     print('insert', "*"*10)
    #     column = data[0]
    #     insert_sql = '''insert into shares_list ( '''+','.join(column)+''' ) value %s '''
    #     data = data[1]
    #     print(insert_sql)
    #     print(data)
    #     ret = cs.execute(insert_sql, (data,))
    #     db.commit()
    # else:
    #     return
    # try:
    #     ret = cs.execute(insert_sql, data)
    #     db.commit()
    #     print('1'*50)
    #     return ret
    # except:
    #     db.rollback()
    #     print('2'*50)
    #     return 0


def get_shares(cs):
    select_sql1 = '''select shares_code_A from shares_list'''
    select_sql2 = '''select shares_code_B from shares_list'''
    ret1 = cs.execute(select_sql1)
    if ret1:
        result1 = list(cs.fetchall())
    else:
        result1 = []
    ret2 = cs.execute(select_sql2)
    if ret2:
        result2 = list(cs.fetchall())
    else:
        result2 = []
    result1.extend(result2)
    return [i[0] for i in result1]


def finished_shares(cs):
    select_sql = '''SELECT DISTINCT company_code FROM `company_product`'''
    cs.execute(select_sql)
    return [i[0] for i in cs.fetchall()]


def check_db(cs, data, table):
    if table == 'finance_info':
        check_sql1 = 'select * from finance_info where share_code=%s and year=%s'
        ret2 = cs.execute(check_sql1, data)
        ret3 = cs.fetchone() if ret2 else None
#     elif table == 'company_notice':
#         check_sql2 = 'select * from company_notice where detail_url=%s'
#         ret2 = cs.execute(check_sql2, [data])
#         ret3 = cs.fetchone() if ret2 else None
#     elif table == 'shares_list':
#         check_sql3 = '''select * from shares_list where company_code=%s'''
#         ret2 = cs.execute(check_sql3, [data])
#         ret3 = cs.fetchone() if ret2 else None
#     else:
#         return
    return ret2, ret3


# def change_company_name(db, cs, column, data):
#     insert_sql = '''insert into abbreviated_change %s value %s'''
#     cs.execute(insert_sql, [column, data])
#     db.commit()


def update_data(db, cs, params):
    # data_str = ','.join(['='.join(i) for i in zip(params[0], params[1])])
    column = list(params[0])
    # column.pop(0)
    column.pop(-2)
    column = [i+'=%s' for i in column]
    data = list(params[1])
    data.pop(-2)
    data.pop(0)
    share_code = data.pop(1)
    year = data.pop(2)
    # company_code = data.pop(0)
    data.append(share_code)
    data.append(year)
    update_sql = 'update finance_info set '+','.join(column)+' where share_code=%s and year=%s'
    # print(update_sql)
    # print(a,b)
    cs.execute(update_sql,data)
    db.commit()


# def is_delete(db, cs):
#     select_sql = '''select company_code,create_time from shares_list where exchange="深交所"'''
#     cs.execute(select_sql)
#     data = cs.fetchall()
#     # print(data)
#     # data = [[i[0],datetime.strftime(i[1],"%Y-%m-%d")] for i in data]
#     # print('*'*30,data)
#     data = [[i[0], datetime.strftime(i[1],"%Y-%m-%d").split(' ')[0].split('-')[-1]] for i in data]
#     # print(data)
#     date_last = [i[1] for i in data]
#
#     # print(date_last)
#     count = list(dict(Counter(date_last)).items())
#     # print(count)
#     is_del = sorted(count, key=lambda x: x[1])
#     is_del.pop()
#     if is_del:
#         is_del = [i[0] for i in is_del]
#         new_data = [[1, i[0]] for i in data if set(is_del) | set(i)][0]
#         delete_sql = '''update shares_list set is_delete=%s where company_code=%s'''
#         cs.execute(delete_sql, new_data)
#         db.commit()
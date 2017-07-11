import pymysql
import platform
from Config import config
import os

user = config.user
psw = config.psw
db_name = config.db_name

if "Windows" in platform.platform():
    backup_tool = config.btool_win
    restore_tool = config.rtool_win
elif "Darwin" in platform.platform():
    backup_tool = config.btool
    restore_tool = config.rtool


def backup_db(target):
    """
    :param target:  target for backup the database
    :return: null
    """
    command = '%s -h%s -u%s -p%s %s > %s' % (backup_tool, config.host, user, psw, db_name, target)
    try:
        os.system(command)
    except Exception as e:
        print(e)


def restore_db(source):
    """
    :param source:  the source for restore the sql data from specified location to the destination database.
    :return: null
    """
    command = '%s -h%s -u%s -p%s -P3306 %s < %s' % (restore_tool, config.host, user, psw, db_name, source)
    try:
        os.system(command)
    except Exception as e:
        print(e)


def exec_sql(sql, db=None):
    """
    :param sql: sql language for query / update / add /delete for the test.
    :param db: database
    :return:  data for query , null for update/delete and id or other key for add.
    """
    try:
        if db:
            conn = pymysql.connect(host=config.host, user=user,  passwd=psw, port=config.port, db=db)
        else:
            conn = pymysql.connect(host=config.host, user=user, passwd=psw, port=config.port, db=db_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        r = cur.fetchall()
        cur.close()
        conn.close()
        return r
    except Exception as e:
        print('Mysql Error %d: %s' % (e.args[0], e.args[1]))


# if __name__ == "__main__":
#     # fd = os.path.join(os.path.dirname(__file__), "backup.sql")
#     #     # restore_db(fd)
#     # print exec_sql("select industry_id from store where store_no=21", "posdb")
#     import time
#
#     start = time.strftime("%Y-%m-%d 00:00:00")
#     end = time.strftime("%Y-%m-%d 23:59:59")
#     pid_list = exec_sql("select id from product where user_id = {0} and create_time between \"{1}\" and \"{2}\""
#                         .format(10, start, end), "product")
#     # print pid_list
#     product_list = []
#     for each in pid_list:
#         # product_list.append(each[0])
#         spec = exec_sql("select id from product_spec where product_id = {0}".format(each[0]), "product")
#         # print spec
#         if spec:
#             exec_sql("delete from product_groupspec where from_spec_id= {0} ".format(spec[0][0]), "product")
#             exec_sql("delete from product_groupspec where to_spec_id= {0}".format(spec[0][0]), "product")
#         exec_sql("delete from reports_dailystock where product_id={0}".format(each[0]), "product")
#         exec_sql("delete from product_mo_list where product_id={0}".format(each[0]), "product")
#         exec_sql("delete from product_flow where product_id={0}".format(each[0]), "product")
#         exec_sql("delete from product_spec where product_id={0}".format(each[0]), "product")
#         exec_sql("delete from product where id={0}".format(each[0]), "product")
#     # print product_list
#     # restore_db("backup.sql")

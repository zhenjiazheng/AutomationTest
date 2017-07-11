# coding=UTF-8

"""
Author: Zheng.zhenjia
"""

import requests
import random
from Config import config
from Common.util import decode_str
from Common.sql import exec_sql
import sys
from imp import reload
reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable

domin = config.preData["pos_url"]
# domin = "http://172.16.0.206/"
supplierId = 101


def login():
    # print("运营后台登录：")
    url = domin + "/py/backend/v1/auth/login/"
    data = {"username": "root", "password": "root1234"}
    ret = requests.post(url, json=data)
    # print ret.json()
    token = ret.json()["data"]["token"]
    return token


def create_store(type):
    print("创建店铺：")
    url = domin + "/py/backend/v1/store/stores/"
    token = login()
    # print token
    headers = {"token": token}
    mobile = "13812345678"
    contact_idcard = random.choice([["杨正祥", "533527198909210238"], ["杨文军", "330224196702265835"], ["姚海林", "452722197507190776"]])
    print contact_idcard
    # + "".join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 7)).replace(' ', '')
    # idcard = "4402211111" + "".join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 8)).replace(' ', '')
    strore_name = "Test" + "".join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 3)).replace(' ', '')
    house_number = "12" + "".join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 3)).replace(' ', '')
    industry = random.randint(1, 11)
    data = {
        "province": "广东省",
        "city": "深圳市",
        "business_license": "http://7xjpiw.com1.z0.glb.clouddn.com//appidbossut5hn5/004a0277998442f29c7987dc051677a1.png",
        "district": "宝安区",
        "store_name": strore_name,
        "house_number": house_number,
        "industry": industry,
        "telephone": "%s" % mobile,
        "longitude": 113.899,
        "cell": "思微simplywork(飞扬科技园)",
        "contact_tel": "%s" % mobile,
        "store_category": type,
        "many": True,
        "idcard_no": "%s" % contact_idcard[1],
        "idcard_set": [
            "http://7xjpiw.com1.z0.glb.clouddn.com//appidbossut5hn5/004a0277998442f29c7987dc051677a1.png",
            "https://www.baidu.com/",
            "http://7xjpiw.com1.z0.glb.clouddn.com//appidbossut5hn5/004a0277998442f29c7987dc051677a1.png",
        ],
        "latitude": 22.566,
        "pos_status": "WORKING",
        "contact_name": contact_idcard[0],
        "storekeeper": contact_idcard[0]
    }
    print(decode_str(data))
    ret = requests.post(url, json=data, headers=headers)
    print(ret.text)
    if str(ret.status_code).startswith("2"):
        # print("Add store %d PASS." % i)
        storeId = ret.json()["data"]["id"]
        print("店铺ID为：{0}".format(storeId))
        return storeId, mobile


# def supplierPasswordReset(token, store):
#     print("\n重置密码获取密码")
#     headers = {"token": token}
#     url = domin + "py/backend/v1/store/stores/{0}/reset-psw/".format(
#             store)
#     print url
#     ret = requests.put(url, headers=headers)
#     print(ret.text)
#     if str(ret.status_code).startswith("2"):
#         text = ret.json()['data']['text']
#         tel = text[text.find('管理员用户名：')+7:text.find('管理员用户名：')+18]
#         password = text[text.find('管理员密码：')+6:text.find('管理员密码：')+12]
#         print(tel, password)
#         return tel, password

def supplierPasswordReset(store):
    md5_123456 = "e10adc3949ba59abbe56e057f20f883e"
    command = "UPDATE store_employee SET password = \"{0}\" where store_id = {1}".format(md5_123456, store)
    command2 = "SELECT login_tel from store_employee where store_id = {0}".format(store)
    db = "posdb"
    exec_sql(command, db)
    password = "123456"
    tel = exec_sql(command2, db)[0][0]
    return tel, password


def supplierLogin(storeNo):
    print("供应商登录")
    # token = login()
    val = supplierPasswordReset(storeNo)
    print storeNo
    tel = val[0]
    password = val[1]
    url = domin + "/py/supplier/v1/auth/login/"
    data = {"password": password,
            "store_id": storeNo,
            "tel": tel
            }
    ret = requests.post(url, json=data)
    print(ret.text)
    if str(ret.status_code).startswith("2"):
        token_supplier = ret.json()["data"]["local_token"]
        print("获取token:" +token_supplier)
        return "token:"+token_supplier


def getStandardCategory(token):
    url = domin + "/py/supplier/v1/product/categories/standard/"
    headers = {"token": token}
    ret = requests.get(url, headers=headers)
    if str(ret.status_code).startswith("2"):
        # print ret.json()["data"]
        categoryId = random.choice(ret.json()["data"])["id"]
        return categoryId


def getDealProduct(token):
    # categoryId = getStandardCategory(token)
    print("获取Deal product list")
    url = domin + "/py/supplier/v1/product/deals/"
    data = {"search": "1234", "limit": 200}
    print data
    headers = {"token": token}
    ret = requests.get(url, params=data, headers=headers)
    print ret.content
    val = ret.json()["data"]["data"]
    li = random.choice(val)
    print(li)
    barcode = li["barcode"]
    print("Barcode {0}".format(barcode))
    return barcode


def supplierAddproduct():
    storeId, tel = create_store(1)
    # print storeId
    url = domin + "/py/supplier/v1/product/products/"
    token = login()
    token_supplier = supplierLogin(storeId)
    print token_supplier
    headers = {"token": token_supplier}
    barcode = getDealProduct(token_supplier)
    print("开始添加商品")
    data = {

            "barcode": barcode,
            "specs": [{
                "purchase_price": "0.01",
                "sale_price": "0.1",
                "stock": 100}],
            "status": 0
            }
    print(data)
    ret = requests.post(url, json=data, headers=headers)
    print(ret.text)
    if str(ret.status_code).startswith("2"):
        print("供应商添加标准商品通过")
        print(ret.json())
        pid1 = ret.json()["data"]["id"]
        specId1 = ret.json()["data"]["specs"][0]["id"]
        print("商品ID：{0}，规格ID：{1}，供应商ID{2}，编码barcode{3}".format(pid1, specId1, storeId, barcode))
        return pid1, specId1, storeId, barcode, token_supplier, tel

if __name__ == "__main__":
    # create_store()
    for i in range(1):
        supplierAddproduct()
        # create_store(0)

    # setPassword(166)
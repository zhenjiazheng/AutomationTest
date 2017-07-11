# -*- coding: utf-8 -*-
# __author__ = 'zhengandy'

from Config import config
import requests
from Common.util import decode_str, random_str
from Common.sql import exec_sql
from HelpScript import dataReady
import random
import sys
from imp import reload
reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


class RunPublic(object):
    def __init__(self):
        pass

    @staticmethod
    def backendLogin(context):
        print("运营后台登录：")
        url = config.preData["pos_url"] + "py/backend/v1/auth/login"
        print("请求地址：" + url)
        data = {"username": "root", "password": "root1234"}
        print("请求参数：")
        print(decode_str(data))
        ret = requests.post(url, json=data)
        if str(ret.status_code).startswith("2"):
            print("返回：")
            print ret.text
            context.key_value.update({"token": ret.json()["data"]["token"]})
            return True
        else:
            print("登录失败")
            print(ret.text)
            return False

    @staticmethod
    def getStoreIdFromList(context, *args):
        print("\n获取store列表：")
        url = config.preData["pos_url"] + "py/backend/v1/store/stores/?limit=15&store_category=0"
        print("请求地址：" + url)
        headers = {"token": context.key_value["token"]}
        print("请求头: ")
        print(headers)
        ret = requests.get(url,  headers=headers)
        if str(ret.status_code).startswith("2"):
            # print("返回：")
            # print decode_str(ret.json()["data"]["data"])
            if args:
                context.key_value.update({"store_id": ret.json()["data"]["data"][args[0]]["id"],
                                      "tel": ret.json()["data"]["data"][args[0]]["telephone"]})
            else:
                context.key_value.update({"store_id": ret.json()["data"]["data"][8]["id"],
                                          "tel": ret.json()["data"]["data"][8]["telephone"]})
            print(context.key_value)
            return True
        else:
            print("获取列表失败")
            print(ret.text)
            return False

    @staticmethod
    def getSupplierIdFromList(context, *args):
        print("\n获取store列表：")
        url = config.preData["pos_url"] + "py/backend/v1/store/stores/?limit=15&store_category=1"
        print("请求地址：" + url)
        headers = {"token": context.key_value["token"]}
        print("请求头: ")
        print(headers)
        ret = requests.get(url, headers=headers)
        if str(ret.status_code).startswith("2"):
            # print("返回：")
            # print decode_str(ret.json()["data"]["data"])
            if args:
                context.key_value.update({"supplier_id": ret.json()["data"]["data"][args[0]]["id"],
                                          "supplier_tel": ret.json()["data"]["data"][args[0]]["telephone"]})
            else:
                context.key_value.update({"supplier_id": ret.json()["data"]["data"][10]["id"],
                                      "supplier_tel": ret.json()["data"]["data"][10]["telephone"]})
            print(context.key_value)
            return True
        else:
            print("获取列表失败")
            print(ret.text)
            return False

    @staticmethod
    def bossLogin(context, *args):
        print("BOSS登录：")
        url = config.preData["pos_url"] + "ja/v1/boss/login"
        print("请求地址：" + url)
        password = "123456"
        data = {
            "password": password,
            "storeNo": context.key_value["store_id"],
            "telephone": context.key_value["tel"]
            }
        print("请求参数：")
        print(decode_str(data))
        ret = requests.post(url, json=data)
        if str(ret.status_code).startswith("2"):
            print("返回：")
            print ret.text
            context.key_value.update({"token_boss": ret.json()["data"]["token"]})
            print(context.key_value)
            return True
        else:
            print("BOSS登录失败")
            print(ret.text)
            return False

    @staticmethod
    def supplierLogin(context, *args):
        print("Supplier登录：")
        url = config.preData["pos_url"] + "py/supplier/v1/auth/login/"
        supplier_id = None
        supplier_tel = None
        print("请求地址：" + url)
        if "supplier_id" in context.key_value:
            supplier_id = context.key_value["supplier_id"]
            supplier_tel = context.key_value["supplier_tel"]
        elif "new_store_id" in context.key_value:
            supplier_id = context.key_value["new_store_id"]
            supplier_tel = context.key_value["supplier_tel"]
        password = "123456"
        data = {
            "password": password,
            "store_id": supplier_id,
            "tel": supplier_tel
            }
        print("请求参数：")
        print(decode_str(data))
        ret = requests.post(url, json=data)
        if str(ret.status_code).startswith("2"):
            print("返回：")
            print ret.text
            context.key_value.update({"token_supplier": ret.json()["data"]["local_token"]})
            print(context.key_value)
            return True
        else:
            print("Supplier登录失败")
            print(ret.text)
            return False

    @staticmethod
    def posLogin(context, *args):
        print("POS机登录：")
        url = config.preData["pos_url"] + "ja/pos/v1/login"
        print("请求地址：" + url)
        storeId = context.key_value["store_id"]
        password = "123456"
        data = {
                "pos_info": {
                    "pos_no": "080027400cba",
                    "pos_type": "Google Nexus 9 - 5.0.0 - API 21 - 1536x2048",
                    "pos_version": "1.0",
                    "rom_version": "3.10.0-genymotion-g08e528d",
                    "system_version": "5.0"
                },
                "pwd": password,
                "shop_no": storeId,
                "username": context.key_value["tel"]
            }
        print("请求参数：")
        print(decode_str(data))
        ret = requests.post(url, json=data)
        if str(ret.status_code).startswith("2"):
            print("返回：")
            print ret.text
            context.key_value.update({"token_pos": ret.json()["data"]["token"], "posNo": data["pos_info"]["pos_no"]})
            print(context.key_value)
            return True
        else:
            print("Pos登录失败")
            print(ret.text)
            return False

    @staticmethod
    def setPassword(context, *args):
        md5_123456 = "e10adc3949ba59abbe56e057f20f883e"
        store_id = []
        if "new_store_id" in context.key_value:
            store_id.append(context.key_value["new_store_id"])
        elif "store_id" in context.key_value:
            store_id.append(context.key_value["store_id"])
        elif "supplier_id" in context.key_value:
            store_id.append(context.key_value["supplier_id"])
        db = "posdb"
        if args:
            command = "UPDATE store_employee SET password = \"{0}\" where store_id = {1}".format(md5_123456, args[0])
            exec_sql(command)
        for each in store_id:
            command = "UPDATE store_employee SET password = \"{0}\" where store_id = {1}".format(md5_123456, each)
            try:
                exec_sql(command, db)
                context.key_value.update({"password": "123456"})
                print context.key_value
                return True
            except Exception, e:
                print e
                return False

    @staticmethod
    def get1productCommodityList(context, *args):
        print("\n\nBoss get one product from list")
        url = config.preData["pos_url"] + "ja/v1/boss/commodity/list?is_standard=true"
        print("请求Url：")
        print url
        headers = {"token": context.key_value["token_boss"], "storeNo": "%d" % context.key_value["store_id"]}
        print("请求头：")
        print headers
        ret = requests.get(url, headers=headers)
        if str(ret.status_code).startswith("2"):
            print("The return data is:")
            print(ret.text)
            if args:
                context.key_value.update({"pid": ret.json()["data"]["data"][args[0]]["id"],
                                          "specId": ret.json()["data"]["data"][args[0]]["specs"][0]["id"],
                                          "purchase_price": ret.json()["data"]["data"][args[0]]["specs"][0]["purchase_price"],
                                          "sale_price": ret.json()["data"]["data"][args[0]]["specs"][0]["sale_price"],
                                          "stock": ret.json()["data"]["data"][args[0]]["specs"][0]["stock"],
                                          "categoryId": ret.json()["data"]["data"][args[0]]["category"],
                                          "barcode": ret.json()["data"]["data"][args[0]]["barcode"],
                                          "category_name": ret.json()["data"]["data"][args[0]]["category_display"]
                                          })
            else:
                context.key_value.update({"pid": ret.json()["data"]["data"][0]["id"],
                                          "specId": ret.json()["data"]["data"][0]["specs"][0]["id"],
                                          "purchase_price": ret.json()["data"]["data"][0]["specs"][0]["purchase_price"],
                                          "sale_price": ret.json()["data"]["data"][0]["specs"][0]["sale_price"],
                                          "stock": ret.json()["data"]["data"][0]["specs"][0]["stock"],
                                          "categoryId": ret.json()["data"]["data"][0]["category"],
                                          "barcode": ret.json()["data"]["data"][0]["barcode"],
                                          "category_name": ret.json()["data"]["data"][0]["category_display"]
                                          })
            print(context.key_value)
            return True
        else:
            print("获取其中一个商品失败")
            print(ret.status_code)
            return False

    @staticmethod
    def addProduct(context, *args):
        print("\n\nBoss Add the product")
        url = config.preData["pos_url"] + "ja/v1/boss/commodity/add"
        print("请求Url：")
        print url
        headers = {"token": context.key_value["token_boss"], "storeNo": "%d" % context.key_value["store_id"]}
        print("请求头：")
        print headers
        data = {
            "status": 0,
            "barcode": "12345678909876",
            "brand": "test",
            "category": 510,
            "is_standard": False,
            "desc_url": "http://www.baidu.com/",
            "image": "http://www.baidu.com/",
            "manufacturer": "manufacturer",
            "moList": [],
            "name": "忍者",
            "price": "122",
            "quality_period": 0,
            "shortcut": 1,
            "source": "面包",
            "specs": [{
                "discount_price": "110",
                "member_price": "110",
                "purchase_price": "100",
                "unit": "100",
                "stock": "100",
                "sale_price": "120"
            }],
            "tag": [],
            "user_id": context.key_value["store_id"],
            "weighable": False
        }
        # print(context.key_value)
        print("请求参数:")
        print(decode_str(data))
        ret = requests.post(url, json=data, headers=headers)
        if str(ret.status_code).startswith("2"):
            print("The return data is:")
            print(ret.text)
            context.key_value.update({"pid1": ret.json()["data"]["id"],
                                      "specId1": ret.json()["data"]["specs"][0]["id"],
                                      "categoryId": 510, "barcode": "12345678909876", "category_name":
                                          ret.json()["data"]["category_display"]
                                      })
            print(context.key_value)
            return True
        else:
            print("添加商品失败")
            print(ret.status_code)
            return False

    @staticmethod
    def addProduct2(context, *args):
        print("\nBoss Add the product 2")
        url = config.preData["pos_url"] + "ja/v1/boss/commodity/add"
        print("请求Url：")
        print url
        headers = {"token": context.key_value["token_boss"], "storeNo": "%d" % context.key_value["store_id"]}
        print("请求头：")
        print headers
        data = {
            "status": 0,
            "barcode": "12345678904321",
            "brand": "test",
            "category": 510,
            "desc_common": "This is the test.",
            "desc_url": "http://www.baidu.com/",
            "image": "http://www.baidu.com/",
            "is_standard": False,
            "manufacturer": "manufacturer",
            "moList": [],
            "name": "忍者222",
            "price": "122",
            "quality_period": 0,
            "shortcut": 1,
            "source": "面包",
            "user_id": context.key_value["store_id"],
            "specs": [{
                "discount_price": "110",
                "member_price": "110",
                "purchase_price": "100",
                "unit": "100",
                "stock": "100",
                "sale_price": "120"
            }],
            "sale_net": False,
            "stock": 100,
            "tag": [],
            "sale_price": "122",
            "weighable": False
            }
        print("请求参数:")
        print(decode_str(data))
        ret = requests.post(url, json=data, headers=headers)
        if str(ret.status_code).startswith("2"):
            print("The return data is:")
            print(ret.text)
            context.key_value.update({"pid2": ret.json()["data"]["id"],
                                      "specId2": ret.json()["data"]["specs"][0]["id"],
                                      "categoryId": 510, "barcode": "12345678904321", "category_name":
                                          ret.json()["data"]["category_display"]})
            print(context.key_value)
            return True
        else:
            print("添加商品失败")
            print(ret.status_code)
            return False

    @staticmethod
    def createSupplier(context, *args):
        print("\n创建供应商")
        headers = {"token": context.key_value["token"]}
        print("请求头：")
        print headers
        url = config.preData["pos_url"] + "py/backend/v1/store/stores/"
        print("请求URL：")
        print url
        data = {
                "telephone": config.preData["MUser2"],
                "business_license": "http://7xjpiw.com1.z0.glb.clouddn.com//"
                                    "appidbossut5hn5/004a0277998442f29c7987dc051677a1.png",
                "city": "深圳市",
                "district": "宝安区",
                "house_number": "504",
                "idcard_no": "533527198909210238",
                "idcard_set": ["https://www.baidu.com/", "http://7xjpiw.com1.z0.glb.clouddn.com//appidbossut5hn5/004a0"
                                                        "277998442f29c7987dc051677a1.png"],
                "storekeeper": "杨正祥",
                "cell": "思微simplywork(飞扬科技园)",
                "store_name": "Test_Supplier_" + "".join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9',
                                                                        '0'], 8)).replace(' ', ''),
                "latitude": 22.566,
                "province": "广东省",
                "store_category": 1,
                "pos_status": "WORKING",
                "address": "广东省深圳市翻身(地铁站)503",
                "industry": 8,
                "longitude": 113.899,
                "contact_name": "TestName",
                "contact_tel": config.preData["MUser2"],
                "many": True
            }
        print("The request param:")
        print(decode_str(data))
        ret = requests.post(url, json=data, headers=headers)
        if str(ret.status_code).startswith("2"):
            print("The return data is:")
            print(ret.text)
            context.key_value.update({"new_store_id": ret.json()["data"]["id"], "supplier_tel": config.preData["MUser2"]})
            print(context.key_value)
            return True
        else:
            print("创建供应商失败。")
            print(ret.status_code)
            return False

    @staticmethod
    def getDealProduct(context, *args):
        print("获取Deal product list")
        url = config.preData["pos_url"] + "/py/supplier/v1/product/deals/"
        data = {"search": "1234", "limit": 200}
        print data
        headers = {"token": context.key_value["token_supplier"]}
        ret = requests.get(url, params=data, headers=headers)
        if str(ret.status_code).startswith("2"):
            val = ret.json()["data"]["data"]
            li = random.choice(val)
            # print(li)
            barcode = li["barcode"]
            print("Barcode {0}".format(barcode))
            # return barcode
            context.key_value.update({"barcode": barcode})
            print context.key_value
            return True
        else:
            return False

    @staticmethod
    def supAddProduct(context, *args):
        url = config.preData["pos_url"] + "/py/supplier/v1/product/products/"
        print("请求URL：")
        headers = {"token": context.key_value["barcode"]}
        print("开始添加商品")
        data = {

                "barcode": context.key_value["barcode"],
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
            # print("商品ID：{0}，规格ID：{1}，供应商ID{2}，编码barcode{3}".format(pid1, specId1, storeId, barcode))
            context.key_value.update(
                {"pid1": pid1, "specId1": specId1})
            return True
        else:
            return False

    @staticmethod
    def createSuppAddProduct(context, *args):
        pid1, specId1, storeId, barcode, token_supplier, tel = dataReady.supplierAddproduct()
        if pid1:
            context.key_value.update({"pid1": pid1, "specId1": specId1, "new_store_id": storeId,
                                  "barcode": str(barcode), "token_supplier": token_supplier, "tel": tel})
            return True
        else:
            return False

    @staticmethod
    def bossSubmitOrder(context, *args):
        print("\nBOSS 提交订单：")
        print(context.key_value)
        headers = {"token": context.key_value["token_boss"], "storeNo": context.key_value["store_id"]}
        print headers
        url = config.preData["pos_url"] + "ja/v1/boss/purchase/order/submit"
        print url
        data = context.key_value["data"]
        data.update({"payWay": 0})
        print(decode_str(data))
        ret = requests.post(url, json=data, headers=headers)
        if str(ret.status_code).startswith("2"):
            print("返回：")
            print ret.text
            order_id = ret.json()['data']
            context.key_value.update({"orderId": order_id})
            print(context.key_value)
            return True
        else:
            print("BOSS 提交订单失败")
            print(ret.text)
            return False

    @staticmethod
    def posGetMemberInfo(context, *args):
        print("\nPOS获取会员信息：")
        print(context.key_value)
        headers = {"token": context.key_value["token_pos"]}
        print headers
        url = config.preData["pos_url"] + "/ja/pos/v1/member/{0}".format(context.key_value["member_id"])
        print url
        ret = requests.get(url, headers=headers)
        member_sale = ret.json()["data"]
        return member_sale

    @staticmethod
    def pos_SyncCart(context, *args):
        print("\nPOS机同步购物车：")
        print(context.key_value)
        data = {}
        headers = {"token": context.key_value["token_pos"]}
        print headers
        url = config.preData["pos_url"] + "ja/pos/v1/sync"
        print url
        ret = requests.get(url, headers=headers)
        if str(ret.status_code).startswith("2"):
            print("返回：")
            print ret.text
            print{"\n\n"}
            sync_data = ret.json()["data"]["sync_data"]
            for item in sync_data:
                if item["key"] == "product":
                    product_list = item["values"]
                    product0 = product_list[0]
                    specs = product0.pop("specs")
                    product0.update(specs[0])
                    product0.update({"sale_cnt": "1", "special_price": specs[0]["sale_price"], "special_price_type": 0,
                                     "special_price_type_tip": "普通价格", "isManySpecs": False, "is_weighing": 0,
                                     "item_type": 0, "seari_num": 0})
                    data.update({"current_order_item": product0, "order_item": [product0]})
                    print product0

                if item["key"] == "staff":
                    staff = item["values"][0]
                    data.update({"cashier_id": staff["staff_id"], "cashier_name": staff["staff_name"]})
            deal_amount = float(specs[0]["sale_price"]) * float(product0["sale_cnt"])
            order_no = random.randint(20, 20)
            data.update({"deal_amount": str(deal_amount), "fullreduced_amount": "0.00", "orderLocal": 1,
                         "order_amount": str(deal_amount), 	"order_no": str(order_no),
                         "order_time": "04-21 04:50:07", "total_discount_amount": "0.00",
                         "member_first_order": False, "store_type": 0})
            print("\nPOS获取会员信息：")
            print(context.key_value)
            url = config.preData["pos_url"] + "/ja/pos/v1/member/{0}".format(context.key_value["member_id"])
            print url
            ret = requests.get(url, headers=headers)
            member_sale = ret.json()["data"]
            data.update({"member_sale": member_sale})
            print("*" * 100)
            print(data)
            print("*" * 100)
            url = config.preData["pos_url"] + "ja/pos/v1/synccart"
            print url
            ret = requests.post(url, json=data, headers=headers)
            print ret.json()
            if ret.json()["status_code"] == 0 or ret.json()["msg"] == "同步购物车成功":
                return True
        else:
            print("POS机同步购物车失败")
            print(ret.text)
            return False


class Context(object):
    """
    Define the Context to store the return value.
    """
    def __init__(self):
        self.key_value = {}

if "__main__" == __name__:
    test = RunPublic()
    context = Context()
    # test.backendLogin(context)
    # if test.getSupplierIdFromList(context):
    #     print("PASS")
    # else:
    #     print("FAIL")

    # context.key_value.update({"store_id": 166, "password": "123456", "tel":"13622123456", "member_id": 44})
    # test.posLogin(context)
    # if test.pos_SyncCart(context):
    #     print "PASS"
    # test.setPassword(context)

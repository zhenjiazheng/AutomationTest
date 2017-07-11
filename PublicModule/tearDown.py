# -*- coding: utf-8 -*-
# __author__ = 'zhengandy'

from Common.sql import exec_sql
import traceback
import time


def tear_down(context, *args):
    sqlist = []
    start = time.strftime("%Y-%m-%d 00:00:00")
    end = time.strftime("%Y-%m-%d 23:59:59")
    try:
        if "store_id" in context.key_value.keys():
            storeId = context.key_value["store_id"]
            sqlist.extend([
                {"command": "delete from points_rule where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from coupon_rule where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from recharge_rule where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from specialoffer_rule where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from product_split_rule where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from fullreduced_rule where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from store_customer where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from set_meal where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from store_customer where store_customer_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from kitchen_printer where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from kitchen_printer_binding where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from barcode_scale where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from inventory_record where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from store where add_storeid={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from user_category where user_id={0}".format(int(storeId)), "db": "product"},
                {"command": "delete from balance_detail where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from coupon_item where store_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from store_customer where store_customer_id={0}".format(int(storeId)), "db": "posdb"},
                {"command": "delete from product_unit where user_id={0}".format(int(storeId)),"db": "product"},
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])
            pid_list = exec_sql("select id from product where user_id = {0} and create_time between \"{1}\" and \"{2}\""
                                .format(storeId, start, end), "product")
            for each in pid_list:
                spec = exec_sql("select id from product_spec where product_id = {0}".format(each[0]), "product")
                if spec:
                    exec_sql("delete from product_groupspec where from_spec_id= {0} ".format(spec[0][0]), "product")
                    exec_sql("delete from product_groupspec where to_spec_id= {0}".format(spec[0][0]), "product")
                exec_sql("delete from reports_dailystock where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_mo_list where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_flow where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_spec where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product where id={0}".format(each[0]), "product")

            order_list = exec_sql("select id from pos_order where member_id = {0}".format(storeId), "posorder")
            for each in order_list:
                exec_sql("delete from orderitem where order_id={0}".format(each[0]), "posorder")
                exec_sql("delete from pos_order where id={0}".format(each[0]), "posorder")

        if "new_store_id" in context.key_value.keys():
            NewStoreId = context.key_value["new_store_id"]
            sqlist.extend([
                {"command": "delete from store_employee where store_id = {0}".format(int(NewStoreId)), "db": "posdb"},
                {"command": "delete from business_license where store_id= {0}".format(int(NewStoreId)), "db": "posdb"},
                {"command": "delete from idcard where store_id={0}".format(int(NewStoreId)), "db": "posdb"},
                {"command": "delete from store where id={0}".format(int(NewStoreId)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])
            pid_list = exec_sql("select id from product where user_id = {0} and create_time between \"{1}\" and \"{2}\""
                                .format(10, start, end), "product")
            for each in pid_list:
                spec = exec_sql("select id from product_spec where product_id = {0}".format(each[0]), "product")
                if spec:
                    exec_sql("delete from product_groupspec where from_spec_id= {0} ".format(spec[0][0]), "product")
                    exec_sql("delete from product_groupspec where to_spec_id= {0}".format(spec[0][0]), "product")
                exec_sql("delete from reports_dailystock where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_mo_list where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_flow where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_spec where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product where id={0}".format(each[0]), "product")

        if "new_store_id2" in context.key_value.keys():
            NewStoreId2 = context.key_value["new_store_id2"]
            sqlist.extend([
                {"command": "delete from store_employee where store_id = {0}".format(int(NewStoreId2)), "db": "posdb"},
                {"command": "delete from business_license where store_id= {0}".format(int(NewStoreId2)), "db": "posdb"},
                {"command": "delete from idcard where store_id={0}".format(int(NewStoreId2)), "db": "posdb"},
                {"command": "delete from store where id={0}".format(int(NewStoreId2)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])
            pid_list = exec_sql("select id from product where user_id = {0} and create_time between \"{1}\" and \"{2}\""
                                .format(10, start, end), "product")
            for each in pid_list:
                spec = exec_sql("select id from product_spec where product_id = {0}".format(each[0]), "product")
                if spec:
                    exec_sql("delete from product_groupspec where from_spec_id= {0} ".format(spec[0][0]), "product")
                    exec_sql("delete from product_groupspec where to_spec_id= {0}".format(spec[0][0]), "product")
                exec_sql("delete from reports_dailystock where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_mo_list where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_flow where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product_spec where product_id={0}".format(each[0]), "product")
                exec_sql("delete from product where id={0}".format(each[0]), "product")

        if "adsId" in context.key_value.keys():
            adsId = context.key_value["adsId"]
            sqlist.extend([
                {"command": "delete from market_weekend where ad_id={0}".format(int(adsId)), "db": "posdb"},
                {"command": "delete from market_bannerimage where ad_banner_id = "
                            "(select id from market_adbanner where ad_id = {0})".format(int(adsId)), "db": "posdb"},
                {"command": "delete from market_adbanner where ad_id={0}".format(int(adsId)), "db": "posdb"},
                {"command": "delete from market_adschedule where ad_id={0}".format(int(adsId)), "db": "posdb"},
                {"command": "delete from market_ad where id={0}".format(int(adsId)), "db": "posdb"}
                ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "ad_holder_id" in context.key_value.keys():
            ad_holder_id = context.key_value["ad_holder_id"]
            sqlist.extend([
                {"command": "delete from market_advertiser where id={0}".format(int(ad_holder_id)), "db": "posdb"}
                ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "ad_holder_id2" in context.key_value.keys():
            ad_holder_id2 = context.key_value["ad_holder_id2"]
            sqlist.extend([
                {"command": "delete from market_advertiser where id={0}".format(int(ad_holder_id2)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "member_id" in context.key_value.keys():
            memberId = context.key_value["member_id"]
            sqlist.extend([
                {"command": "delete from store_member where id={0}".format(int(memberId)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "member_id2" in context.key_value.keys():
            memberId2 = context.key_value["member_id2"]
            sqlist.extend([
                {"command": "delete from store_member where id={0}".format(int(memberId2)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "tableId" in context.key_value.keys():
            tableId = context.key_value["tableId"]
            sqlist.extend([{"command": "delete from store_table where id={0}".format(int(tableId)), "db": "posdb"}])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "tableId2" in context.key_value.keys():
            tableId2 = context.key_value["tableId2"]
            sqlist.extend([{"command": "delete from store_table where id={0}".format(int(tableId2)), "db": "posdb"}])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "unit_id" in context.key_value.keys():
            unit_id = context.key_value["unit_id"]
            sqlist.extend([{"command": "delete from product_unit where id={0}".format(int(unit_id)), "db": "product"}])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "employeeId1" in context.key_value.keys():
            employeeId1 = context.key_value["employeeId1"]
            sqlist.extend([
                {"command": "delete from store_employee where id={0}".format(int(employeeId1)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "categoryId1" in context.key_value.keys():
            categoryId1 = context.key_value["categoryId1"]
            sqlist.extend([
                {"command": "delete from category where id={0}".format(int(categoryId1)), "db": "product"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "categoryId2" in context.key_value.keys():
            categoryId2 = context.key_value["categoryId2"]
            sqlist.extend([
                {"command": "delete from category where id={0}".format(int(categoryId2)), "db": "product"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "orderId" in context.key_value.keys():
            orderId = context.key_value["orderId"]
            sqlist.extend([
                {"command": "delete from refund_order where order_id={0}".format(int(orderId)), "db": "posorder"},
                {"command": "delete from orderitem where order_id={0}".format(int(orderId)), "db": "posorder"},
                {"command": "delete from pos_order where id={0}".format(int(orderId)), "db": "posorder"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "makeId" in context.key_value.keys():
            makeId = context.key_value["makeId"]
            sqlist.extend([
                {"command": "delete from product_mo_list where modusoperandi_id = {0}".format(makeId), "db": "product"},
                {"command": "delete from product_modusoperandi where id={0}".format(int(makeId)), "db": "product"}

            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "supplier_id" in context.key_value.keys():
            supplier_id = context.key_value["supplier_id"]
            sqlist.extend([
                {"command": "delete from boss_supplier where id= {0}".format(int(supplier_id)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "supplier_id2" in context.key_value.keys():
            supplier_id2 = context.key_value["supplier_id2"]
            sqlist.extend([
                {"command": "delete from boss_supplier where id= {0}".format(int(supplier_id2)), "db": "posdb"}
            ])
            for each in sqlist:
                exec_sql(each["command"], each["db"])

        if "supplier_id3" in context.key_value.keys():
            supplier_id3 = context.key_value["supplier_id3"]
            sqlist.extend([
                {"command": "delete from boss_supplier where id= {0}".format(int(supplier_id3)), "db": "posdb"}
            ])
            for each in sqlist:
                # print each
                exec_sql(each["command"], each["db"])

        if "addressId" in context.key_value.keys():
            addressId = context.key_value["addressId"]
            sqlist.extend([
                {"command": "delete from address where id= {0}".format(int(addressId)), "db": "posdb"}
            ])
            for each in sqlist:
                # print each
                exec_sql(each["command"], each["db"])

        sqlist = [
            {"command": "delete from software_update_strategy where url=\"{0}\"".format(
                        "http://www.baidu.com/"), "db": "posdb"},
            {"command": "delete from auth_user where username=\"test\"",
                 "db": "posdb"},
            {"command": "delete from market_advertiser where name = \"广告主名称\"", "db": "posdb"},
            {"command": "delete from store_member where telephone = \"13423412789\"", "db": "posdb"},
            {"command": "delete from store_member where telephone = \"13500044444\"", "db": "posdb"},
            {"command": "delete from product_unit where name = \"test\" or name = \"你好吗\" or name = \"测试分类\"",
             "db": "product"},
            {"command": "delete from store_employee where employee_name = \"TestEmp\"", "db": "posdb"},
            {"command": "delete from store_employee where employee_name = \"TestEmp2\"", "db": "posdb"},
            {"command": "delete from address where phone=\"13423412789\"", "db": "posdb"}
            ]
        for each in sqlist:
            exec_sql(each["command"], each["db"])
    except Exception, e:
        print e
        traceback.print_exc()
        print sqlist


class Context(object):
    """
    Define the Context to store the return value.
    """
    def __init__(self):
        self.key_value = {}

if "__main__" == __name__:
    context = Context()
    tear_down(context)
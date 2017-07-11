# -*- coding: utf-8 -*-
# __author__ = 'zhengandy'
#

import os
from Common.util import md5_s, base64_encode, get_device, get_apk_path, random_str
import datetime

# """
# Below is the Environment Settings
# """

platf = os.environ.get('platform', 'api')
item = os.environ.get('UT_ITEM', 0)
items = os.environ.get("CASELIST", "")
folder = os.environ.get('projectCaseFolder', "Cases/API/POS/BOSS/IncomeProduct")
email =os.environ.get('email', 0)
testlist = os.environ.get("testlist", "")

# """
# Below is the email configuration:
# """
email_sender = "automation-notification@hey900.com"
email_sender_password = "Setup2017"
smtp_sever = "smtp.exmail.qq.com"

email_cc = ["joe.du@hey900.com", "gene.gu@hey900.com", "cs@hey900.com", "develop@hey900.com"]
if "POS" in folder:
    email_receiver = ["pos@hey900.com", "pos_develop@hey900.com", "tangwei.tang@hey900.com", "clark.li@hey900.com"]

elif "JiHe" in folder:
    email_receiver = ["jhjrdevelop@hey900.com", "jinhui.zhou@hey900.com"]

# """
# Below is the database config
# """
# db = os.environ.get('DATABASE', "waiwang")

if "JiHe" in folder:
    host = "120.24.169.76"
    user = "dev"
    psw = "ZP0wEuGG8Mxk"
    port = 3306
    db_name = "waiwang"
elif "POS" in folder:
    host = '172.16.0.52'
    port = 5306
    user = 'postest'
    psw = 'DJdg@903902901'
    db_name = 'posdb'
else:
    host = '172.16.0.52'
    port = 5306
    user = 'postest'
    psw = 'DJdg@903902901'
    db_name = 'posdb'

btool = '/usr/local/mysql/bin/mysqldump'
rtool = '/usr/local/mysql/bin/mysql'
btool_win = 'E:/mysql-5.6.17-winx64/bin/mysqldump'
rtool_win = 'E:/mysql-5.6.17-winx64/bin/mysql'


# """
# Below is the desired_caps for all platform
# """

# app = '/Users/AndyZheng/workspace/others/Custom-debug.apk'
if platf == "android":
    app = get_apk_path()
    android_package = get_apk_path()
    udid = get_device()  # '9LSOLNKBTC7P5HAA'  # 'LE67A06310200851'

platformVersion = '10.1'
deviceName = 'iPhone 6'
iosApp = '/Users/AndyZheng/Desktop/iOS-app-bootstrap.app'
# iosApp = '/Users/AndyZheng/Desktop/ZzwaterDealer.app'
iosUdid = 'D16160E4-6921-44FD-AD85-1C7C771FDD3B'
package = 'com.geometry.posboss'
# activity = 'com.github.android_app_bootstrap.activity.WelcomeActivity'

android_activity = "xxxxxx"
iOS_bundleId = "xxxxxx"
if "POS" in folder:
    desktop_url = 'http://devtest-pos.thy360.com/backend_web/views/userlogin.html'
if "JIHEPC" in folder:
    desktop_url = 'https://dev-www.jihe365.cn/'
else:
    desktop_url = 'http://devtest-pos.thy360.com/backend_web/views/userlogin.html'
# desktop_url = 'https://www.baidu.com'
# """
# Below is the API config
# """
method = os.environ.get('METHOD', "DEBUG")
# method = "DEBUG"
# filepath = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")), "test1.jpg")
# print filepath
preData = {
    "zzkg_merchant_release_url": "http://testauto.thy360.com/",
    "jh_url": "https://dev-m.jihe365.cn/",
    "zzkg_admin_url": "http://172.16.6.213/",
    "zzkg_url": "http://172.16.0.207/",
    "zzkg_merchant_url": "http://release-console.thy360.com/",
    "xsd_user_url": "http://172.16.0.70/",
    "xsd_user_release": "http://xsd-release.thy360.com/",
    "hyb_url": "http://release.thy360.com/",
    "hyb_bs": "https://hyb-console-dev.thy360.com/bao",
    "pos_url": "http://devtest-pos.thy360.com/",
    # "pos_url": "http://devnew-pos.thy360.com/",
    "servicePhone":"13432132144",
    "sqwm_url": "http://172.16.0.207/",
    "sqwm_user1": "15507554489",
    "new_password": "123456",
    "BDCRMUser": "joedu",
    "BDCRMPassword": "root@01",
    "ZZKGAdminUser1": "leoli",
    "ZZKGAdminUser1Pass": "123456",
    "zzkg_test_user": "15814982521",
    "User1": "17711111022",
    "User2": "17711111010",
    "User3": "13664581232",
    "User4": "15215123525",
    "User": "13500044444",
    "MUser1": "13798765888",
    "MUser2": "13798765777",
    "JRUser": "18682090783",
    "JRUser1": "18682090784",
    "JRUser2": "18682090771",
    "JRUser3": "18682090772",
    "User6": "15423441212",
    "JRUser4": "73682333358",
    "JRUser5": "18682090580",

    "NUser":"13510952139",
    "NUserForBank":"13265404902",
    "NUserForBank1":"73602553036",
    "UserForGift":"17700000002",
    "UserForQuiPayS":"17072869340",
    "UserForQuiPayF":"18682090770",
    "UserForEmpPay":"13760357015",
    "IFriendUser": "13782090783",

    "UserForEmpInvRec": "13510952312",
    "UserForAlwNew": "13510951000",
    "UserForConName": "13510951001",
    "UserForNone": "13510951002",
    "UserForBorCompEmp":"13510951003",
    "UserForBorCompEx":"13510951004",

    "InvFriForP": "13510952009",
    "InvFriForP2": "13510952008",
    "InvFriForI": "13510952001",
    "InvFriForV": "13322983973",
    "InvFriRefuse": "13510952002",
    "InvFriWait": "13166110195",


    "123456": md5_s("123456"),
    "Admin": "13511111111",
    "Admin2": "13522222222",
    "Admin3": "13533333333",
    "deliveryType": 10,
    "POS_User": "13423412789",
    "POS_User1": "18682090783",
    "day": datetime.datetime.now().strftime("%Y-%m-%d"),
    "Password": "123456",
    "mobile": "15000000000",
    "cate_store_id": 41,
    "orderNo": random_str("012345678901234567890", 17),
    "store_name": random_str("abcdefghijklmnopqrstuvwxyz")
}

if "JiHe" in folder:
    filename = "uploadedFile"
else:
    filename = "uploadedFile"



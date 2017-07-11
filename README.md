一. macaca 框架安装步骤：
1. 安装JDK，下载地址：http://www.oracle.com/technetwork/java/javase/downloads/index.html
2. JDK环境变量配置JAVA_HOME
3. 安装Nodejs 下载地址:https://nodejs.org/en/download/
4. 安装配置macaca：
	npm config set registry https://registry.npm.taobao.org
	npm install macaca-cli -g
	npm install macaca-electron -g
	npm install macaca-android -g
	npm install macaca-chrome  -g
	npm install macaca-chromedriver  -g
5. 配置ANT，下载地址：http://ant.apache.org/manualdownload.cgi
6. 安装配置Android SDK
具体可参考：https://teste
rhome.com/topic/6272

二. 自动化工程python所需依赖库
执行命令：
pip install -r requirements.txt


三．工程项目运行方法：

工程项目运行方法：

cd到对应的存放路径

在根部目录下运行命令行：

python main.py -P arg0 -F arg1 -N arg2 -S arg3 -P args4 -DB args5 -CL args6

例子：
python main.py -P "api" -F "Projects/JiHe" -N 1 -S 1 -P "Projects／JiHePre" -DB "waiwang" -CL "1,2,4,7,9"

如果想运行几何金融项目的1，2，4，7，9：
python main.py -P "api" -F "Projects/JiHe" -DB "waiwang" -CL "1,2,4,7,9"

支持多文件夹用例执行：
python main.py -P "api" -F "Projects/JiHe/UserInterface; Projects/JiHe/account; Projects/JiHe/public"
此命令执行的用例为UserInterface; account; public三个文件夹的所有用例，适合用于一个项目中有多个模块用例
特别注意：-F 后面所带的多个文件夹必须用"; "隔开；

-F M-必选
-N 可选，默认0（全部用例）
-S 可选 默认0 （延时表示）
-P 可选 默认 None（预设置公共步骤）如无不需要带
-DB 可选 默认"waiwang"--几何金融的数据库 （ 由于每个项目使用的数据库不一样，这部分单独参数化 ，如在测试步骤中不需要对数据库操作无需
                                        理会）
-CL 可选 默认"" --此参数与-N互斥，优先-N。

做API接口测试的相关人员对于写json的用例熟悉。

范例:
{
	"input":{
			"method": "POST",
			"url":"http://release.thy360.com/",
			"rest": "py/dealer/backend/v5/seller/login/",
			"headers": null,
			"param":{
				"phoneNumber":"13924595452", "password": "123456"
			}
	},
  "output":{ "msg": {"EQ":"【成功】"}, "dealer_token": {"TYPE":"str"}, "business_type_id": {"EQ":4}
      },
  "key": ["dealer_token"] 或者 "key": {key: value}
}

SQL范例：
{
	"sql":[
		"delete from users where id = {{key.uid}}",
		"delete from users_verified where user_id = {{key.uid}}",
		"delete from users_extend where user_id = {{key.uid}}",
		"delete from account_invest where user_id = {{key.uid}}",
		"delete from account_invest_record where user_id = {{key.uid}}"
	]
}

如果有select出现需要保存数据时，范例：
{
	"sql":[
		"select id from users where mobile = {{pre.User1}}"
	],
	"key": ["id"]
}

 redis范例：
 {
	"redis":{
		"delete":"key1",
		"set":{ "key2": "value2","key3": "value3"},
		"flushall":null,
		"size": null,
		"get":["name","name1"]
	}，
	"key": ["name","name1"]
}

其中input是接口请求的部分,包括请求的地址(url+rest), headers在这里是会带上用户或商户登录后产生的token。
param为请求报文。

output这里是为了检查每个返回值的类型/具体值/或者其他定义的校验值。如不需要校验可以不带或为空对象
可以直接具体到每个值
例如：
{
	"input":{
			"method": "GET",
			"url":"{{pre.jh_url}}",
			"rest": "ja/v1/test/sms/regist?",
			"headers":{"client": "lj_android",
                        "Content-Type": "application/json"
				},
			"param":{
				"phone":"{{pre.User1}}", "code": "1234"
			}
	},
  "output":{"code": {"ALLIN":[0,"1234"]},"msg":{"TYPE":"str"}, "data":{"TYPE":"dict"}，"data.code":{"EQ":"1234"} },
  "key":{"code":"data.code"}   # 将data.code返回保存为key值为code
}

key为在当前步骤需要保存的某个返回key值对应的value, 如果保存之前已经有当前key值存在,当前的key,value对会被更新替换。如不需要保存key可以
不带此健或为空。

UI 测试用例范本：

两种形式都支持
1.
{
  "author": "test",
  "caseStep": {
    "1": "input element by id, value com.geometry.posboss:id/et_store_no, text test",
    "2": "input element by id, value com.geometry.posboss:id/et_user, text test",
    "3": "input element by id, value com.geometry.posboss:id/et_password, text test",
    "4": "click element by id, value com.geometry.posboss:id/cb_choose_agreement",
    "5": "compare element by id, value com.geometry.posboss:id/et_store_no, attribute text, expected abc",
    "6": "long press element by id , value com.geometry.posboss:id/xxx, duration 2",
    "7": "check after delete element by name, vale 登录",
    "8": "get title, expect hello world",
    "9": "find element by id, value com.geometry.posboss:id/et_store_no",
    "10": "long press element by id, value com.geometry.posboss:id/et_store_no, duration 2",
    "11": "drag driver from x:100 y:100 to x:200 y:200",
    "12": "drag element by id, value com.geometry.posboss:id/cb_choose_agreement to x:200 y:200",
    "13": "press system keyEvent:4 sleep 5"
  }
}

2.
{
  "author": "test",
  "caseStep": {
    "1": {
      "operation": "文本输入",
      "by": "id",
      "value": "com.geometry.posboss:id/et_store_no",
      "text":"Test"
    },
    "2": {
      "operation": "文本输入",
      "by": "id",
      "value": "com.geometry.posboss:id/et_user",
      "text":"Test"
    },
    "3":{
      "operation": "文本输入",
      "by": "id",
      "value": "com.geometry.posboss:id/et_password",
      "text":"Test"
    },
    "4": {
      "operation": "点击控件",
      "by": "id",
      "value": "com.geometry.posboss:id/cb_choose_agreement"
    },
    "5":{
     "operation": "点击控件",
      "by" : "name",
      "value": "登录"
    }
  }
}


目前支持的各类封装规则：
{
  "author": "test",
  "caseStep": {
    "1": "input element by id, value com.geometry.posboss:id/et_store_no, text test",
    "2": "input element by id, value com.geometry.posboss:id/et_user, text test",
    "3": "input element by id, value com.geometry.posboss:id/et_password, text test",
    "4": "click element by id, value com.geometry.posboss:id/cb_choose_agreement",
    "5": "compare element by id, value com.geometry.posboss:id/et_store_no, attribute text, expected abc",
    "6": "long press element by id , value com.geometry.posboss:id/xxx, duration 2",
    "7": "check after delete element by name, vale 登录",
    "8": "get title, expect hello world",
    "9": "find element by id, value com.geometry.posboss:id/et_store_no",
    "10": "long press element by id, value com.geometry.posboss:id/et_store_no, duration 2",
    "11": "drag driver from x:100 y:100 to x:200 y:200",
    "12": "drag element by id, value com.geometry.posboss:id/cb_choose_agreement to x:200 y:200",
    "13": "press system keyEvent:4 sleep 5",
    "14": "wait for element by id, value com.geometry.posboss:id/et_store_no, time 4",
    "15": "accept alert",
    "16": "dismiss alert",
    "17": "check alert text expect 确定",
    "18": "get current context",
    "19": "get current windows",
    "20": "find elements by id, value com.geometry.posboss:id/et_store_no",
    "21": "tap location x:100 y:200",
    "22": "double tap x:100 y:200",
    "23": "double tap element by id, value com.geometry.posboss:id/et_store_no",
    "24": "continue touch driver from x:100 y:100 to x:100,200,300,400 y:100,200,300,400"
  }
}


四．最后关于如何定时运行工程对项目进行回归测试：
python apsch.py argv[1] argv[2]

其中argv[0]为第一个输入的python文件。
-- argv[1]为独立运行python main.py的对应命令，例如："python main.py -P \"android\" -PF \"Case/android\" -N 1"
-- argv[2]为定期执行该命令的间隔时间。
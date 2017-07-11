# coding=UTF-8
# __author__ = 'andy.zheng'

import simplejson
from jinja2 import Template
import os
import re
import unittest
import time
from Common.util import decode_str
from Config import config
from Common.driver_init import init
import sys
import platform
import threading
from imp import reload
reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


def get_sys_platform():
    if "Darwin" in platform.platform():
        return "OSX"
    if "Windows" in platform.platform():
        return "WINDOWS"
    if "Linux" in platform.platform():
        return "Linux"
    else:
        pass


def printout(content=None):
    if get_sys_platform() == "OSX" or "Linux":
        print(content.encode("utf-8"))
    if get_sys_platform() == "WINDOWS":
        print(content.encode("GBK"))


class Context(object):
    """
    Define the Context to store the return value.
    """
    def __init__(self):
        self.key_value = {}


def template_json(filename):
    """
    :param filename:  接口用例步骤文件,json文件.
    :return:  返回读取的的数据.
    """
    value = open(filename).read()
    try:
        t = Template(value)
        value = t.render(pre=config.preData)
    except Exception as e:
        print(e)
        return False
    value = simplejson.loads(value)
    return value


def capture_screen(driver, filename):
    driver.save_screenshot(filename)


def check_data(driver, filename):
    """
    最后执行的关键步骤，请求输入，输出检查。
    :param driver: init driver
    :param filename: 用例文件绝对路径
    :return:  布尔（True或者False）
    """
    val = template_json(filename)
    if "author" in val.keys():
        print("测试用例编写责任人：{0}".format(val["author"]))
    case_steps = sorted(val["caseStep"].keys())
    case_name = filename.split(".json")[0].split("\\")[-2] + ".png"
    dirname = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Report", "ScreenShot"))
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    pic = time.strftime("%Y%m%d%H%M") + ".png"
    sc_name = os.path.join(dirname, pic)
    print sc_name
    for i, each in enumerate(case_steps):
        print("执行步骤{0}:".format(i+1))
        print(decode_str(val["caseStep"][each]))
        in_value = val['caseStep'][each]
        if isinstance(in_value, basestring):
            try:
                if "click element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    driver.element(by, value).click()

                elif "input element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+),.*text (?P<text>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    text = m1.group('text')
                    driver.element(by, value).send_keys(text)

                elif "wait for element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+),.*time (?P<time>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    wt = m1.group('time')
                    driver.wait_for_element(by, value, wt)

                elif "compare element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+),.*attribute(?P<attribute>.+), .*expected'
                                  u' (?P<expect>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    text = m1.group('text')
                    driver.element(by, value).send_keys(text)

                elif "find element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    driver.element_if_exists(by, value)

                elif "check after delete element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    try:
                        driver.element(by, value)
                        return False
                    except Exception, e:
                        print("Element already delete.")
                        print(e)
                elif "get title" in in_value:
                    m1 = re.match(u'.*expect (?P<expect>.+)', in_value)
                    expect = m1.group('by')
                    if not driver.title == expect:
                            print("对应的真实值与期望不相符合。")
                            return False
                elif "long press element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+),.*duration (?P<duration>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    duration = int(m1.group('value'))
                    driver.element(by, value).touch("press", {"duration": duration})

                elif "drag driver" in in_value:
                    m1 = re.match(u'.*from x:(?P<x1>.+) .*y:(?P<y1>.+).*to x:(?P<x2>.+) .*y:(?P<y2>.+)', in_value)
                    startX = m1.group('x1')
                    startY = m1.group('y1')
                    endX = m1.group('x2')
                    endY = m1.group('y2')
                    driver.touch("drag", {startX, startY, endX, endY})

                elif "tap location" in in_value:
                    m1 = re.match(u'.*x:(?P<x>.+) .*y:(?P<y>.+)', in_value)
                    x = m1.group('x')
                    y = m1.group('y')
                    driver.touch("tap", {x, y})

                elif "double tap" in in_value:
                    if "element" in in_value:
                        m1 = re.match(u'.*by:(?P<by>.+), .*value:(?P<value>.+)', in_value)
                        by = m1.group('by')
                        value = m1.group('value')
                        x = m1.group('x')
                        y = m1.group('y')
                        driver.element(by, value).touch("doubleTap")
                    else:
                        m1 = re.match(u'.*x:(?P<x>.+) .*y:(?P<y>.+)', in_value)
                        x = m1.group('x')
                        y = m1.group('y')
                        driver.touch("doubleTap", {x, y})
                elif "continue touch driver":
                    m1 = re.match(u'.*from x(?P<FX>.+).*y(?P<FY>.+) to .*x(?P<TX>.+).*y(?P<TY>.+)', in_value)
                    fx = m1.group("FX")
                    fy = m1.group("FY")
                    tx = m1.group("TX")
                    ty = m1.group("TY")
                    x_list = tx.split(",")[1:]
                    y_ist = ty.split(",")[1:]
                    a_list = [{"drag", {"fromX": fx, "fromY": fy, "toX": tx, "toY": ty}}]
                    for k in range(len(x_list)):
                        s_l = {"drag", {"toX": x_list[k], "toY": y_ist[k]}}
                        a_list.append(s_l)
                    driver.touch(a_list)
                elif "drag element" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+).*to x:(?P<x1>.+) .*y:(?P<y1>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    x = m1.group('x1')
                    y = m1.group('y1')
                    driver.element(by, value).touch("drag", {"toX": x, "toY": y})

                elif "accept alert" in in_value:
                    driver.accept_alert()

                elif "dismiss alert" in in_value:
                    driver.dismiss_alert()

                elif "check alert text":  # For ios only
                    m1 = re.match(u'.*expect (?P<expect>.+)', in_value)
                    expect = m1.group('expect')
                    if driver.alert_text == expect:
                        print("检查Alert Text通过")
                    else:
                        print driver.alert_text
                        return False
                elif "get current context":
                    print driver.context

                elif "get current windows":
                    print driver.current_window_handle

                elif "find elements" in in_value:
                    m1 = re.match(u'.*by (?P<by>.+),.*value (?P<value>.+)', in_value)
                    by = m1.group('by')
                    value = m1.group('value')
                    driver.elements(by, value)

                elif "press system keyEvent" in in_value:
                    m1 = re.match(u'.*keyEvent:(?P<code>.+)', in_value)
                    code = m1.group('code')
                    os.system("adb shell input keyevent %d" % int(code))

                if "sleep" in in_value:
                    m1 = re.match(u'.*sleep (?P<sleep>.+)', in_value)
                    sleep = m1.group('sleep')
                    time.sleep(int(sleep))
            except Exception as e:
                capture_screen(driver, sc_name)
                print e
                return False
        elif isinstance(in_value, dict):
            try:
                if "控件是否存在" in in_value["operation"]:
                    driver.element_if_exists(in_value["by"], in_value["value"])
                if "点击控件" in in_value["operation"]:
                    driver.element(in_value["by"], in_value["value"]).click()
                if "最大化" in in_value["operation"]:
                    driver.maximize_window()
                if "滚动" in in_value["operation"]:
                    js = "var q=document.documentElement.scrollTop=10000"
                    driver.execute_script(js)
                if "文本输入" in in_value["operation"]:
                    driver.element(in_value["by"], in_value["value"]).send_keys(in_value["text"])
                if "控件属性" in in_value["operation"]:
                    if in_value["attribute"] == "text":
                        if not driver.element(in_value["by"], in_value["value"]).text == in_value["expectText"]:
                            print("对应的Attribute与期望不相符合。")
                            return False
                if "控件操作Touch" in in_value["operation"]:
                    print(in_value["method"], in_value["parameter"])
                    if in_value["method"] == "press":
                        print("This is the press method.")
                        driver.element(in_value["by"], in_value["value"]).touch("press", {"duration": 2})
                    elif in_value["method"] == "drag":
                        print("This is the drag method")
                        if "by" in in_value.keys():
                            driver.element(in_value["by"], in_value["value"]).touch('drag', {"toX": in_value["endX"],
                                                                                             "toY": in_value["endY"]})
                        else:
                            driver.element("drag", {in_value["startX"], in_value["startY"], in_value["endX"],
                                                    in_value["endY"]})
                    else:
                        print("cannot find")
                if "控件校验不存在" in in_value["operation"]:
                    try:
                        driver.element(in_value["by"], in_value["value"])
                        return False
                    except Exception, e:
                        print("Element already delete.")
                        print(e)
                if "系统按钮key event" in in_value["operation"]:
                    os.system("adb shell input keyevent %d" % in_value["keyCode"])
                if "页面标题" in in_value["operation"]:
                    if not driver.title == in_value["expectText"]:
                            print("对应的真实值与期望不相符合。")
                if "弹窗提醒" in in_value["operation"]:
                    if "by" in in_value.keys():

                            return False
                if "sleep" in in_value.keys():
                    time.sleep(in_value['sleep'])
            except Exception, e:
                capture_screen(driver, sc_name)
                print(e)
                return False
        # print("步骤{0}通过。".format(i+1))
    return True


def case_list(case_path):
    """
    此方法为了方便后面的test用例名获取显示
    :param case_path: 用例的绝对路径
    :return:  所有用例的列表
    """
    for root, dirs, files in os.walk(case_path):
        cases = dirs
        return cases


def get_test_steps(path_dir, case):
    """
    :param path_dir: 工程根目录路径。
    :param case:  用例名称，从case_list中获取。单纯的取其中一个。
    :return: 获取输入测试用例的所有测试步骤。
    """
    for root, dirs, files in os.walk(os.path.join(path_dir, case)):
        steps = []
        for each in files:
            each = os.path.join(os.path.join(path_dir, case), each)
            steps.append(each)
        return steps


def check_case(driver, cases):
    """
    运行所有测试用例的使用方法。
    :param driver: init driver。
    :param cases: 所有测试用例列表。
    :return: 返回检查结果（boolean）
    """
    sleep_time = float(os.environ.get('SLEEP_TIME', 0))
    mark = 0
    for x, item in enumerate(cases, 1):
        print("-"*100)
        if check_data(driver,  item):
            mark += 1
        else:
            print("The test if Fail.\n" + "-"*100)
            return False
        print("-"*100+"\n")
        time.sleep(sleep_time)
    if mark == len(cases):
        return True


class RunServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cmd = 'macaca server --verbose'

    def run(self):
        os.system(self.cmd)
        time.sleep(5)


def kill_pid():
    pid_all = []
    if get_sys_platform() == "WINDOWS":
        cmd1 = 'Netstat -ano|findstr \"3456\"'
        pids = os.popen(cmd1)
        for each in pids.readlines():
            pid = str(each)[-5:-1]
            if pid not in pid_all:
                pid_all.append(pid)
        for each in pid_all:
            if int(each) != 0:
                cmd2 = 'taskkill /F /PID %s' % each
                os.system(cmd2)
    elif get_sys_platform() == "OSX":
        cmd1 = "lsof -i :3456"
        pids = os.popen(cmd1)
        text = pids.readlines()
        if text:
            for each in text[1:]:
                pid = str(each)[7:13]
                if pid not in pid_all:
                    pid_all.append(pid)
            for each in pid_all:
                if int(each) != 0:
                    cmd2 = 'kill -9  %s' % each
                    os.system(cmd2)
    # elif get_sys_platform() == "Linux":
    #     cmd1 = "netstat -anp | grep 3456"


class UnitTest(unittest.TestCase):
    def setUp(self):
        kill_pid()
        r = RunServer()
        r.setDaemon(True)
        r.start()
        self.driver = init()
        self.driver.set_implicitly_wait(10)
        time.sleep(10)

    def tearDown(self):
        self.driver.quit()
        for i in range(6):
            os.system("adb shell input keyevent 4")
        kill_pid()

    def run_case(self, steps):
        printout("\n测试用例开始时间: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        # for each in allStepList:
        # context = Context()
        self.assertTrue(check_case(self.driver, steps), "Test FAIL.")

    @staticmethod
    def get_test_func(steps):
        """
        :param steps: 测试步骤
        :return: 调用单元测试中的run_case执行测试。
        """
        def func(self):
            self.run_case(steps)
        return func


def __generate_test_cases():
    """
    本地执行产生对应的test suite。
    :return:  产生testsuite 把所有用例传递到UnitTest中的get_test_func进行测试。
    """
    lists = []
    caselist = []
    folder = config.folder  # os.environ.get('projectCaseFolder', "Cases\\API\\POS\\BOSS")
    folders = folder.split("; ")
    for each in folders:
        suite_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), each)
        cases = case_list(suite_dir)
        for item in cases:
            caselist.append(item)
        for j in range(len(cases)):
            steps = get_test_steps(suite_dir, cases[j])
            lists.append(steps)
    item = int(config.item)  # int(os.environ.get('UT_ITEM', 0))
    items = config.items.split(",")  # os.environ.get("CASELIST", "").split(",")
    print('-' * 100)
    if item == -1 and items == [""]:
        for i in range(len(lists)):
            test_func = "test_" + caselist[i]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[i]))
    elif item == -1 and items != [""]:
        for each in items:
            test_func = "test_" + caselist[int(each)-1]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[int(each)-1]))
    elif item != -1 and items == [""]:
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))
    elif item != -1 and items != [""]:
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))

__generate_test_cases()


def suite():
    lists = []
    caselist = []
    folder = config.folder  # os.environ.get('projectCaseFolder', "Cases\\API\\POS\\BOSS")
    folders = folder.split("; ")
    for i, each in enumerate(folders):
        suite_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), each)
        cases = case_list(suite_dir)
        for item in cases:
            caselist.append(item)
        for j in range(len(cases)):
            steps = get_test_steps(suite_dir, cases[j])
            lists.append(steps)
    item = int(config.item)  # int(os.environ.get('UT_ITEM', 0))
    items = config.items.split(",")  # os.environ.get("CASELIST", "").split(",")
    print('-' * 100)
    if item == -1 and items == [""]:
        printout('当前选择所有测试用例执行。')
        for i in range(len(lists)):
            test_func = "test_" + caselist[i]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[i]))
    elif item == -1 and items != [""]:
        printout('当前选择部分测试用例执行：')
        for each in items:
            test_func = "test_" + caselist[int(each)-1]
            setattr(UnitTest, test_func, UnitTest.get_test_func(lists[int(each)-1]))
    elif item != -1 and items == [""]:
        printout('当前选择第%d个用例执行测试。' % (item+1))
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))
    elif item != -1 and items != [""]:
        printout('当前选择第%d个用例执行测试。' % (item+1))
        test_func = "test_" + caselist[item]
        setattr(UnitTest, test_func, UnitTest.get_test_func(lists[item]))
    print('-' * 100)
    suit = unittest.TestSuite()
    suit.addTest(unittest.makeSuite(UnitTest))
    return suit
#
if __name__ == "__main__":
    unittest.main()

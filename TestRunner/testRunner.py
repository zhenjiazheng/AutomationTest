# -*- coding: utf-8 -*-
"""
Author: Zheng.zhenjia
"""

import codecs
from unittest import TestSuite
from HTMLTestRunner import HTMLTestRunner as Tr
from Common.sendEmail import send_email
from Config import config
from testReport import TestReport
# import platform
import os
# cur_path = os.path.dirname(os.path.abspath(__file__))
# print(cur_path)


def test_suite():
    platf = config.platf  # os.environ.get('platform', 'api')
    module_names = ""
    # moduleNames=build_test_suite()
    if platf == "api":
        # if "Windows" in platform.platform():
        #     module_names = ["API"]
        # else:
        module_names = ["ApiExecutor.API"]
    elif platf == "android":
        module_names = ["UiExecutor.UI"]
    elif platf == "iOS":
        module_names = ["UiExecutor.UI"]
    elif platf == "desktop":
        module_names = ["UiExecutor.UI"]
    t_suite = TestSuite()
    # print(t_suite)

    for module_name in module_names:
        # print(module_name)
        import importlib
        m = importlib.import_module(module_name, package=platf)
        # modules=map(__import__,moduleNames)
        t_suite.addTest(m.suite())
        # suite.addTest(element(module.suite()))
    return t_suite


def main():
    email = int(config.email)  # int(os.environ.get('email', 0))
    global report_file, text, runner, fp, report_title
    report_file = TestReport.generate_report("Report")
    runner = Tr()
    fp = codecs.open(report_file, 'wb', 'utf-8')
    report_title = "Report" + "_" + test_suite.__name__
    runner = Tr(stream=fp, verbosity=2, title=report_title, description=report_file)
    runner.run(test_suite())
    fp.close()
    text = TestReport.get_log_path()
    # print text
    if email == 1:
        send_email(report_file, text, config.email_receiver, config.email_cc)
    os.popen("rm {0}".format(text))

if __name__ == '__main__':
    main()

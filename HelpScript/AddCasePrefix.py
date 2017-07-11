# coding=UTF-8

"""
Author: Zheng.zhenjia
"""
import codecs
import os
import platform
import sys
from imp import reload
reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


def case_find(fo):
    curr_path = os.path.abspath(__file__)
    # print curr_path
    cfgfile_dir = os.path.dirname(curr_path)
    # print cfgfile_dir
    fo_path = os.path.realpath(os.path.join(cfgfile_dir,"..", fo))
    # print fo_path
    return cfgfile_dir, fo_path

print case_find("Case\\api")


def instead_string(fo, str1, str2, str3):
    """
    :param fo:  The folder to be operated.
    :param str1:  string will be find in the text.
    :param str2:  string will be instead.
    :param str3:  string be instead of old one.
    :return:
    """
    json = case_find(fo)[1]
    for root, dirs, files in os.walk(json):
        for each in files:
            if each.endswith(".json"):
                each = os.path.abspath(os.path.join(root, each))
                fd = codecs.open(each, 'r', 'utf-8')
                lin = fd.read()
                fd.close()
                fd = codecs.open(each, 'w', 'utf-8')
                if str1 in lin:
                    fd.write(str(lin).replace(str2, str3))
                else:
                    fd.write(str(lin))
                fd.close()

            else:
                pass


def case_prefix(fo, action, str):
    """
    :param fo:  The folder will perform add or reduce number.
    :param action:  1 for add the case number, 2 for reduce the case number
    :return:
    """
    json = case_find(fo)[1]
    # print(json)
    for root, dirs, files in os.walk(json):
        if len(dirs) > 0:
            # print(len(dirs))
            for i in range(len(dirs)):
                if dirs[i]:
                    if action == 1:
                        if "Windows" in platform.platform():
                                os.rename("%s\\%s" % (json, dirs[i]), "%s\\%s" % (json, ("{0}".format(str) + dirs[i])))
                        else:
                                os.rename("%s/%s" % (json, dirs[i]), "%s/%s" % (json, ("{0}".format(str) + dirs[i])))
                    if action == 2:
                        print(len(str))
                        print(len(dirs[i][len(str):]))
                        print(dirs[i][len(str):])
                        # Remove the case number.
                        # print("%s/%s" % (json, dirs[i]))
                        if "Windows" in platform.platform():
                            os.rename("%s\\%s" % (json, dirs[i]), "%s\\%s" % (json, dirs[i][len(str):]))
                        else:
                            os.rename("%s/%s" % (json, dirs[i]), "%s/%s" % (json, dirs[i][len(str):]))

# jsonString("M7",1)｀

if "__main__" == __name__:
    case_prefix("Cases\\API\\POS\\BOSS", 1, "BOSS_")

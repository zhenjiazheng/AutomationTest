# coding=UTF-8

"""
Author: Zheng.zhenjia
"""

# import codecs
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf8')  # @UndefinedVariable


def log(txt, content):
    ch = chardet.detect(content)["encoding"]
    content = content.decode(ch).encode("utf-8")
    fd = open(txt, 'a+')
    fd.write(content)
    fd.close()

# if __name__ == "__main__":
#     log("log.txt", "This is the test333\n")


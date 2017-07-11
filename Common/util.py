# coding=UTF-8
import hashlib
import sys
import simplejson
import base64
import os
from random import Random
from imp import reload
reload(sys)
sys.setdefaultencoding("utf8")  # @UndefinedVariable


def get_values_by_key(input_json, key, values=list):
    key_value = None
    value = None
    if isinstance(input_json, dict):
        for json_result in input_json.values():
            if key in input_json.keys():
                key_value = input_json.get(key)
                if key_value not in values:
                    values.append(key_value)
            else:
                get_values_by_key(json_result, key, values)
    elif isinstance(input_json, list):
        for json_array in input_json:
            get_values_by_key(json_array, key, values)
    if values:
        if len(values) > 1:
            value = values
        elif len(values) == 1:
            value = values[0]
        return value
    else:
        return "Cannot find the value"


def sort_data(di, ignore="Secret Key"):
    """
    此方法为了接口文档中的Headers secret使用
    :param di: 输入参数的params
    :param ignore: 对应的secret key
    :return:
    """
    for k in di.keys():
        if ignore in di.keys():
            di.pop(ignore)
    for k in di.keys():
        if di[k] is None:
            di.pop(k)
    return "".join(["{0}={1}&".format(k, di[k]) for k in sorted(di.keys())])[:-1].encode("utf-8")


def md5_secret(in_str, serect_key):
    """
    MD5加密
    :param in_str:
    :param serect_key:
    :return:
    """
    md_str = in_str+"&secret="+serect_key
    # print md_str
    md = hashlib.md5()
    md.update(md_str)
    md_ret = md.hexdigest().upper()
    return md_ret


def md5_s(in_str):
    """
    MD5加密
    :param in_str:
    :return:
    """
    md_str = in_str
    # print md_str
    md = hashlib.md5()
    md.update(md_str)
    md_ret = md.hexdigest()
    return md_ret


def get_current_stamp():
    import datetime
    import time
    return str(int(time.mktime(datetime.datetime.now().timetuple())))


class OptionalException(Exception):
    pass


def get_value(property_path, data):
    temp = data
    for k in property_path.split("."):
        if k.endswith("?"):
            k = k[:-1]
            is_optional = True
        else:
            is_optional = False

        try:
            idx = int(k)
            try:
                temp = temp[idx]
                # print temp
            except IndexError as e:
                if is_optional:
                    raise OptionalException()
                else:
                    raise e

        except ValueError as e:
            try:
                temp = temp[k]
            except KeyError as e:
                if is_optional:
                    # return None
                    raise OptionalException()
                else:
                    raise e
    return temp


def decode_str(content, encoding='utf-8'):
    # 只支持json格式
    # indent 表示缩进空格数
    return simplejson.dumps(content, encoding=encoding, ensure_ascii=False, indent=4)


def md5_sec(in_str):
    """
    MD5加密
    :param in_str:
    :return:
    """
    # print md_str
    md = hashlib.md5()
    md.update(in_str)
    md_ret = md.hexdigest()
    return md_ret


def base64_encode(content):
    return base64.b64encode(content)


def get_device():
    value = os.popen("adb devices")
    for v in value.readlines():
        s_value = str(v).replace("\n", "").replace("\t", "")
        if s_value.rfind('device') != -1 and (not s_value.startswith("List")) and s_value != "":
            return s_value[:s_value.find('device')].strip()


def get_apk_path():
        """
        get test APK in prjPath
        :return:basename
        """
        ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # print ROOT_DIR
        apks = os.listdir(ROOT_DIR)
        if len(apks) > 0:
            for apk in apks:
                basename = os.path.basename(apk)
                if basename.split('.')[-1] == "apk":
                    apk_path = os.path.abspath(os.path.join(ROOT_DIR, basename))
                    return apk_path
        else:
            return None


def random_str(chars, leng=20):
    str = ''
    # chars = '012345678901234567890'
    # leng = len(chars) - 1
    random = Random()
    for i in range(leng):
        str += chars[random.randint(0, leng)]
    return str

#
# if __name__ == "__main__":
#     print random_orderNo()

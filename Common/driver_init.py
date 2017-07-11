# -*- coding: utf-8 -*-
# __author__ = 'zhengandy'

from macaca import WebDriver
import os
from Config import config
import sys

platform = os.environ.get('platform', "UiExecutor")

if platform == "android":
    desired_caps = {
        'platformName': platform,
        'udid': config.udid,
        'app': config.app if config.app is not None else None,
        'package': config.package,
        'reuse': 3
    }
elif platform == "iOS":
    desired_caps = {
        'platformName': platform,
        'platformVersion': config.platformVersion,
        # 'deviceName': config.deviceName,
        'app': config.iosApp,
        'udid': config.iosUdid,
        'resetKeyboard': True,
        'autoAcceptAlerts': True,
        'reuse': 1
    }
elif platform == "desktop":
    desired_caps = {
        'platformName': platform,
        'browserName': 'electron'
    }
else:
    desired_caps = {}


def init():
    if platform != "api":
        sys.stdout.write("This is the running %s Testing." % platform)
        server_url = {
            'hostname': 'localhost',
            'port': 3456
        }
        print(desired_caps)
        driver = WebDriver(desired_caps, server_url)
        driver.init()
        driver.set_implicitly_wait(10)
        if "desktop" in platform:
            driver.get(config.desktop_url)
        # os.system("adb shell input keyevent 82")
        return driver
    else:
        sys.stdout.write("This is the running API Testing.")


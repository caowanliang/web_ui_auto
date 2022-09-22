#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/27 21:08
# @Author: william.cao
# @File  : conftest.py

import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from common.read_config import ini
from common.read_element import Element
from page_object.login_page import LoginPage

_driver = None

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    获取每个用例状态的钩子函数
    :param item:
    :return:
    """
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # 添加allure报告截图
        with allure.step('添加失败截图...'):
            allure.attach(_driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    global _driver
    if _driver is None:
        # 取消chrom https安全问题
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('headless')  # => 为Chrome配置无头模式
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('disable-gpu')

        service = Service(r'/usr/local/bin/chromedriver')
        # 浏览器初始化
        _driver = webdriver.Chrome(service=service, options=options)
        _driver.maximize_window()

    def fn():
        _driver.quit()
    request.addfinalizer(fn)
    return _driver


@pytest.fixture(scope='class', autouse=True)
def tian_chi_cloud_login(drivers):
    """打开天池云"""
    login = LoginPage(drivers)
    locator = Element('login')
    login.get_url(ini.url)
    login.input_admin(locator=locator['用户名'], content=ini.admin)
    login.input_password(locator=locator['密码'], content=ini.password)
    login.click_login(locator=locator['登陆'])


if __name__ == '__main__':
    tian_chi_cloud_login(drivers)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/27 21:08
# @Author: william.cao
# @File  : conftest.py

import os
import time

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from common.read_config import ReadConfig, ini
from common.read_element import Element
from page_object.login_page import LoginPage

@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    global _driver
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

    # # 清除缓存提示框
    # _driver.get('chrome://settings/clearBrowserData')
    # # 2S 等待时间
    # time.sleep(2)
    # clear_button = _driver.execute_script("return document.querySelector('settings-ui').shadowRoot.querySelector('settings-main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector('settings-section > settings-privacy-page').shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataDialog').querySelector('#clearBrowsingDataConfirm')")
    # clear_button.click()

    def fn():
        _driver.quit()
    request.addfinalizer(fn)
    return _driver


@pytest.fixture(scope='class', autouse=True)
def tian_chi_cloud_login(drivers):
    """登陆/退登天池云"""
    login = LoginPage(drivers)
    locator = Element('login')
    login.get_url(ini.url)
    login.input_admin(locator=locator['用户名'], content=ini.admin)
    login.input_password(locator=locator['密码'], content=ini.password)
    login.click_login(locator=locator['登陆'])
    yield
    login.click_login(locator=locator['用户名片'])
    login.click_login(locator=locator['注销'])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    """
    失败截图并附加到allure报告中
    :return:
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if hasattr(_driver, "get_screenshot_as_png"):
            allure.attach(_driver.get_screenshot_as_png(), "异常截图", allure.attachment_type.PNG)


if __name__ == '__main__':
     tian_chi_cloud_login(drivers)
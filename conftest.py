#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/27 20:39
# @Author: william.cao
# @File  : conftest.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver = None


@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    global driver
    if driver is None:
        # 取消chrom https安全问题
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        service = Service(r'/usr/local/bin/chromedriver')
        # 浏览器初始化
        driver = webdriver.Chrome(service=service, chrome_options=options)
        driver.maximize_window()

    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver

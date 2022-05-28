#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/27 21:08
# @Author: william.cao
# @File  : conftest.py

import base64
import pytest
import allure
from py.xml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from common.read_config import ini
from common.read_element import Element
from config.conf import cm
from page_object.login_page import LoginPage
from untils.send_mail import send_report
from untils.times import timestamp

driver = None


@pytest.fixture(scope='class', autouse=True)
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


@pytest.fixture(scope='class', autouse=True)
def tian_chi_cloud_login(drivers):
    """打开天池云"""
    login = LoginPage(drivers)
    locator = Element('login')
    login.get_url(ini.url)
    login.input_admin(locator=locator['用户名'], content=ini.admin)
    login.input_password(locator=locator['密码'], content=ini.password)
    login.click_login(locator=locator['登陆'])


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = _capture_screenshot()
            if screen_img:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_node_id'))
    cells.pop(2)


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


def pytest_html_report_title(report):
    report.title = "安恒超融合项目UI测试报告"


def pytest_configure(config):
    config._metadata.clear()
    config._metadata['测试项目'] = "安恒超融合"
    config._metadata['测试地址'] = ini.url


def pytest_html_results_summary(prefix, summary, postfix):
    # prefix.clear() # 清空summary中的内容
    prefix.extend([html.p("所属部门: 安恒信息云产品线，测试部")])
    prefix.extend([html.p("测试执行人: 电脑")])


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """收集测试结果"""
    result = {
        "total": terminalreporter._numcollected,
        'passed': len(terminalreporter.stats.get('passed', [])),
        'failed': len(terminalreporter  .stats.get('failed', [])),
        'error': len(terminalreporter.stats.get('error', [])),
        'skipped': len(terminalreporter.stats.get('skipped', [])),
        # terminalreporter._sessionstarttime 会话开始时间
        'total times': timestamp() - terminalreporter._sessionstarttime
    }
    print(result)
    if result['failed'] or result['error']:
        send_report()


def _capture_screenshot():
    """截图保存为base64"""
    now_time, screen_file = cm.screen_path
    driver.save_screenshot(screen_file)
    allure.attach.file(screen_file, "失败截图{}".format(now_time), allure.attachment_type.PNG)
    with open(screen_file, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()


if __name__ == '__main__':
    tian_chi_cloud_login(drivers)

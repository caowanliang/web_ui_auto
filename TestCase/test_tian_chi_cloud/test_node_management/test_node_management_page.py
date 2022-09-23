#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/30 10:58
# @Author: william.cao
# @File  : test_node_management_page.py

import pytest
import allure

from common.read_element import Element
from page.web_page import WebPage


@allure.feature("模块名称_例子")
@allure.title("测试类标题_例子")
@pytest.mark.usefixtures('tian_chi_cloud_login', 'drivers')
class TestTianChiNodeManagementExample:
    """
    @allure.severity装饰器按严重性级别来标记case　　　
    执行指定测试用例 --allure-severities blocker
    BLOCKER = 'blocker'　　阻塞缺陷
    CRITICAL = 'critical'　严重缺陷
    NORMAL = 'normal'　　  一般缺陷
    MINOR = 'minor'　　    次要缺陷
    TRIVIAL = 'trivial'　　轻微缺陷　
    """

    def setup_class(self):
        # 获取页面元素地址
        self.operations_center_element = Element('operations_center')

    @allure.story("新增节点")
    @allure.step("打开运营中心")
    @allure.severity("blocker") # 用例等级
    @allure.testcase("测试用例的禅道链接地址_例子")
    def test_new_add_node(self, drivers):
        self.web_page = WebPage(drivers)
        self.web_page.is_click(locator=self.operations_center_element['运营中心'])
        assert 1==1


if __name__ == '__main__':
    pass


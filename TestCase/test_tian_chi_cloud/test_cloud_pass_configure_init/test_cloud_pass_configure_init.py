#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/30 10:58
# @Author: william.cao
# @File  : test_node_management_page.py

import pytest
import allure

from common.read_element import Element
from page.web_page import WebPage


@allure.feature("测试节点管理模块")
@pytest.mark.usefixtures('tian_chi_cloud_login', 'drivers')
class TestTianChiNodeManagement:
    def setup_class(self):
        # 获取页面元素地址
        self.operations_center_element = Element('operations_center')

    @allure.story("新增节点")
    def test_config_cloud_pass_serverip(self, drivers):
        self.web_page = WebPage(drivers)
        self.web_page.is_click(locator=self.operations_center_element['平台运营'])
        self.web_page.is_click(locator=self.operations_center_element['云通网络'])
        self.web_page.is_click(locator=self.operations_center_element['云通Server信息_配置'])
        self.web_page.input_text(locator=self.operations_center_element['云通Server_KeepAlive_IP输入项'], txt='1.1.1.1/24')
        self.web_page.is_click(locator=self.operations_center_element['取消'])


if __name__ == '__main__':
    pass


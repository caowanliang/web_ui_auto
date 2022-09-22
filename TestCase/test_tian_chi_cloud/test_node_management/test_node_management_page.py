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
    def test_new_add_node(self, drivers):
        pass
        # self.web_page = WebPage(drivers)
        # self.web_page.is_click(locator=self.operations_center_element['运营中心'])
        # assert 1==2


if __name__ == '__main__':
    pass


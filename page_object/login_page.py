#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/27 21:04
# @Author: william.cao
# @File  : login_page.py

from page.web_page import WebPage


class LoginPage(WebPage):
    """登录类"""

    def input_admin(self, locator, content):
        """输入用户名"""
        self.input_text(locator=locator, txt=content)

    def input_password(self, locator, content):
        """输入密码"""
        self.input_text(locator=locator, txt=content)

    def click_login(self, locator):
        """点击登陆"""
        self.is_click(locator)


if __name__ == '__main__':
    pass

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/27 20:57
# @Author: william.cao
# @File  : read_config.py

import configparser
from config.conf import cm

HOST = 'HOST'
ADMIN = 'ADMIN'
PASSWORD = 'PASSWORD'


class ReadConfig(object):
    """配置文件"""

    def __init__(self):
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(cm.ini_file, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(cm.ini_file, 'w') as f:
            self.config.write(f)

    @property
    def url(self):
        return self._get(HOST, HOST)

    @property
    def admin(self):
        return self._get(HOST, ADMIN)

    @property
    def password(self):
        return self._get(HOST, PASSWORD)


ini = ReadConfig()

if __name__ == '__main__':
    print(ini.url)

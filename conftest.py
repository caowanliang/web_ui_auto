#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/27 20:39
# @Author: william.cao
# @File  : conftest.py

import pytest

@pytest.fixture(scope='session', autouse=True)
def drivers():
    pass

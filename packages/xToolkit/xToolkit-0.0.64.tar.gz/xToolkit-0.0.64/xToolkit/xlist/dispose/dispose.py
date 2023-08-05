#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/28 16:28
# @Author  : 熊利宏
# @project : 列表基础模块
# @Email   : xionglihong@163.com
# @File    : dispose.py
# @IDE     : PyCharm
# @REMARKS : 列表基础模块

# 科学计算库
import numpy
import pandas


# 列表基础处理
class Dispose(object):
    """
    列表基础处理
    """

    def __init__(self, mark):
        self.__mark = mark

    # 值的频率
    def values_count(self, *args):
        """
        统计值得出现次数（字典）
        """
        return pandas.value_counts(self.__mark).to_dict()

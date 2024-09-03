#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Sy,Sang"
__version__ = ""
__license__ = "GPLv3"
__maintainer__ = "Sy, Sang"
__email__ = "martin9le@163.com"
__status__ = "Development"
__credits__ = []
__date__ = ""
__copyright__ = ""

# 系统模块
import copy
import pickle
import json
from typing import Union, Self
from collections import namedtuple
import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# 项目模块
from easy_datetime.timestamp import TimeStamp

# 外部模块
import numpy


# 代码块

def timer(func):
    """
    函数计时器
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds to execute")
        return result

    return wrapper


if __name__ == "__main__":
    pass

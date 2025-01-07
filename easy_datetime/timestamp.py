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
import re
import time
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import decimal
from typing import Union, Self

# 项目模块

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


def datetime_delta(d0: datetime, delta_key: str, delta: int) -> datetime:
    """
    通过字符串进行日期加减
    """
    if delta_key == "year":
        d0 += relativedelta(years=delta)
    elif delta_key == "month":
        d0 += relativedelta(months=delta)
    elif delta_key == "day":
        d0 += timedelta(days=delta)
    elif delta_key == "week":
        d0 += timedelta(days=delta * 7)
    elif delta_key == "hour":
        d0 += timedelta(hours=delta)
    elif delta_key == "min":
        d0 += timedelta(minutes=delta)
    elif delta_key == "sec":
        d0 += timedelta(seconds=delta)
    elif delta_key == "microsec":
        d0 += timedelta(microseconds=delta)
    return d0


def init(*args, **kwargs) -> list:
    """初始化时间列表"""
    kdic = {
        "y": 0,
        "m": 1,
        "d": 2,
        "H": 3,
        "M": 4,
        "S": 5,
        "MS": 6
    }
    init_date_int_list = [1, 1, 1, 0, 0, 0, 0]
    if len(args) == 0:
        init_date_int_list = [datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour,
                              datetime.now().minute, datetime.now().second, datetime.now().microsecond]
    elif len(args) == 1:
        arg = args[0]
        if isinstance(arg, datetime):
            init_date_int_list = [args[0].year, args[0].month, args[0].day, args[0].hour, args[0].minute,
                                  args[0].second, args[0].microsecond]
        elif isinstance(arg, str):
            int_list = [int(i) for i in re.findall(r'\d+', args[0])]
            for i, ti in enumerate(int_list):
                init_date_int_list[i] = ti
        elif isinstance(arg, (int, float, decimal.Decimal)):
            if arg >= 31507200:
                temp_dt = datetime.fromtimestamp(args[0])
                init_date_int_list = [temp_dt.year, temp_dt.month, temp_dt.day, temp_dt.hour, temp_dt.minute,
                                      temp_dt.second, temp_dt.microsecond]
            else:
                init_date_int_list = [int(arg), 1, 1, 0, 0, 0, 0]
        elif isinstance(arg, bytes):
            temp_dt = datetime(args[0])
            init_date_int_list = [temp_dt.year, temp_dt.month, temp_dt.day, temp_dt.hour, temp_dt.minute,
                                  temp_dt.second, temp_dt.microsecond]
    elif len(args) == 2:
        if isinstance(args[0], int) and isinstance(args[1], str):
            num_str = str(args[0])
            str_list = ["", "", "", "", "", ""]
            for i, s in enumerate(args[1]):
                if s == "y":
                    str_list[0] += num_str[i]
                elif s == "m":
                    str_list[1] += num_str[i]
                elif s == "d":
                    str_list[2] += num_str[i]
                elif s == "H":
                    str_list[3] += num_str[i]
                elif s == "M":
                    str_list[4] += num_str[i]
                elif s == "S":
                    str_list[5] += num_str[i]
                else:
                    pass
            date_num_list = [int(i) for i in str_list if i != ""]
            temp_dt = datetime(*date_num_list)
            init_date_int_list = [temp_dt.year, temp_dt.month, temp_dt.day, temp_dt.hour, temp_dt.minute,
                                  temp_dt.second, temp_dt.microsecond]
        else:
            init_date_int_list = [int(args[0]), int(args[1]), 1, 0, 0, 0, 0]
    else:
        int_list = [int(i) for i in args]
        for i, ti in enumerate(int_list):
            init_date_int_list[i] = ti

    for i in kwargs.items():
        init_date_int_list[kdic[i[0]]] = i[1]

    return init_date_int_list


class TimeStamp(datetime):
    """
    时间戳类
    """

    def __new__(cls, *args, **kwargs):
        init_list = init(*args, **kwargs)
        return super().__new__(cls, *init_list)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.core = {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "min": self.minute,
            "sec": self.second,
            "microsec": self.microsecond
        }
        self.map = copy.deepcopy(self.core)
        self.map["weekday"] = self.weekday()
        self.map["week"] = int((self.timestamp() - datetime(self.year, 1, 1).timestamp()) / (7 * 86400))
        self.map["month_week"] = int((self.timestamp() - datetime(self.year, self.month, 1).timestamp()) / (7 * 86400))

    @classmethod
    def now(cls, tz=...) -> Self:
        """
        获取当前时间
        :param tz:
        :return:
        """
        return cls(datetime.now())

    def get_date_string(self) -> str:
        """
        获取日期字符串
        :return:
        """
        return str(self).split(" ")[0]

    def get_chinese_date_string(self) -> str:
        """
        获取中文日期
        :return:
        """
        ds = self.get_date_string().split("-")
        return f"{ds[0]}年{ds[1]}月{ds[2]}日"

    def get_chinese_datetime_str(self) -> str:
        """获取中文时间全文"""
        return f"{self.year}年{self.month}月{self.day}日{self.hour}点{self.minute}分{self.second}秒"

    def get_time_string(self) -> str:
        """
        获取时间字符串
        :return:
        """
        return str(self).split(" ")[1]

    def get_date(self) -> Self:
        """
        获取日期
        :return:
        """
        return type(self)(self.year, self.month, self.day)

    def get_date_with_last_sec(self) -> Self:
        """获取当天最后时刻"""
        return type(self)(self.year, self.month, self.day, 23, 59, 59)

    def __getitem__(self, item) -> Union[int, Self, datetime]:
        if isinstance(item, str):
            return self.map[item]
        elif isinstance(item, slice):
            key_list = list(self.map)[item]
            init_list = []
            for k in key_list:
                init_list.append(self.map[k])
            print(init_list)
            return type(self)(*init_list)
        elif isinstance(item, list):
            return [self.map[i] for i in item]
        elif isinstance(item, tuple):
            return type(self)(*[self.map[i] for i in item])

    def __add__(self, other) -> Union[Self]:
        if isinstance(other, (int, float)):
            return type(self)(self.timestamp() + other)
        elif isinstance(other, (tuple, list)):
            temp_datetime = datetime.fromtimestamp(self.timestamp())
            return type(self)(datetime_delta(temp_datetime, other[0], other[1]))
        elif isinstance(other, dict):
            temp_datetime = datetime.fromtimestamp(self.timestamp())
            for k in list(other):
                temp_datetime = datetime_delta(temp_datetime, k, other[k])
            return type(self)(temp_datetime)
        elif isinstance(other, TimeStamp):
            unix_timestamp = self.timestamp() + other.timestamp()
            return type(self)(unix_timestamp)
        elif isinstance(other, timedelta):
            return type(self)(super().__add__(other))
        else:
            temp_datetime = datetime.fromtimestamp(self.timestamp())
            return temp_datetime + other

    def __sub__(self, other) -> Union[Self, int]:
        if isinstance(other, (int, float)):
            return type(self)(self.timestamp() - other)
        elif isinstance(other, (tuple, list)):
            temp_datetime = datetime.fromtimestamp(self.timestamp())
            return type(self)(datetime_delta(temp_datetime, other[0], -1 * other[1]))
        elif isinstance(other, dict):
            temp_datetime = datetime.fromtimestamp(self.timestamp())
            for k in list(other):
                temp_datetime = datetime_delta(temp_datetime, k, -1 * other[k])
            return type(self)(temp_datetime)
        elif isinstance(other, TimeStamp):
            unix_timestamp = self.timestamp() - other.timestamp()
            return unix_timestamp
        elif isinstance(other, timedelta):
            return type(self)(super().__sub__(other))
        else:
            temp_datetime = datetime.fromtimestamp(self.timestamp())
            return temp_datetime - other

    def accurate_to(self, temporal: str) -> Self:
        temporal_map = {
            "year": (self.year),
            "month": (self.year, self.month),
            "day": (self.year, self.month, self.day),
            "hour": (self.year, self.month, self.day, self.hour),
            "min": (self.year, self.month, self.day, self.hour, self.minute),
            "sec": (self.year, self.month, self.day, self.hour, self.minute, self.second),
            "ms": (self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond)
        }
        if temporal not in temporal_map:
            return copy.deepcopy(self)
        else:
            return type(self)(*temporal_map[temporal])

    def sec(self, *args) -> Union[dict, int, list]:
        """
        获取时间戳各节点的秒数
        :return:
        """
        len_dic = dict({})

        len_dic["year"] = (TimeStamp(self.year, 1, 1) + ["year", 1]).timestamp() - TimeStamp(self.year, 1,
                                                                                             1).timestamp()
        len_dic["month"] = TimeStamp(self.year, self.month, 1).timestamp() - TimeStamp(self.year, self.month,
                                                                                       1).timestamp()
        len_dic["week"] = 86400 * 7
        len_dic["day"] = 86400
        len_dic["hour"] = 3600
        len_dic["min"] = 60
        len_dic["sec"] = 1
        len_dic["microsec"] = 1 / 1000000

        if args != ():
            if len(args) == 1:
                return len_dic[args[0]]
            else:
                return [len_dic[a] for a in args]
        else:
            return len_dic

    def days_in_week(self) -> list[Self]:
        """
        获取同一周的所有日
        :return:
        """
        date = self.get_date() - ["day", self.weekday()]
        days = [date + ["day", i] for i in range(7)]
        return [type(self)(i.year, i.month, i.day) for i in days]

    def days_in_month(self) -> list[Self]:
        """
        获取同一月的所有日
        :return:
        """
        days = self.__class__.timestamp_range(
            TimeStamp(self.year, self.month, 1),
            TimeStamp(self.year, self.month, 1) + ["month", 1],
            "day",
            1,
            False
        )
        return [type(self)(i.year, i.month, i.day) for i in days]

    def days_in_year(self) -> list[Self]:
        """
        获取同一年的所有日
        :return:
        """
        days = self.__class__.timestamp_range(
            TimeStamp(self.year, self.month, 1),
            TimeStamp(self.year, self.month, 1) + ["year", 1],
            "day",
            1,
            False
        )
        return [type(self)(i.year, i.month, i.day) for i in days]

    def last_day_in_month(self) -> int:
        """月内最后一天"""
        return self.days_in_month()[-1].day

    def last_day_in_year(self) -> int:
        """年内最后一天"""
        return self.days_in_year()[-1].day

    @classmethod
    def timestamp_range(
            cls,
            first: ("TimeStamp", datetime, str),
            last: ("TimeStamp", datetime, str),
            temporal_expression: str,
            delta: (int, float),
            include_last=False
    ) -> list[Self]:
        """
        获取一个时间范围
        :param first:
        :param last:
        :param temporal_expression:
        :param delta:
        :param include_last:
        :return:
        """
        t0 = first if isinstance(first, TimeStamp) else TimeStamp(first)
        t1 = last if isinstance(last, TimeStamp) else TimeStamp(last)
        t = t0
        range_list = []

        while True:
            if t < t1:
                range_list.append(t)
            elif t == t1 and include_last is True:
                range_list.append(t)
            else:
                break
            t += (temporal_expression, delta)

        return range_list


class TimeLine(object):
    """
    时间线
    """

    def __init__(self, time_list: list = None):
        if time_list is None:
            self.data = []
        else:
            self.data = [TimeStamp(i) for i in time_list]

    def __len__(self) -> int:
        return len(self.data)

    def clone(self, *args, **kwargs) -> list[TimeStamp]:
        """
        拷贝时间轴
        :param args:
        :param kwargs:
        :return:
        """
        return copy.deepcopy(self.data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def timestamp(self) -> list[float]:
        """
        获取该时间轴的unix时间戳
        :return:
        """
        return [i.timestamp() for i in self.data]

    def timestamp_array(self) -> numpy.ndarray:
        """
        获取该时间轴的unix时间戳numpy数组
        :return:
        """
        return numpy.array([i.timestamp() for i in self.data])

    def get_time_slice(self, temporal_expression: str, value: int = 1, operator: str = "=="):
        """
        时间切片获取index
        :param temporal_expression:
        :param value:
        :param operator:
        :return:
        """
        te_list = numpy.array([i.map[temporal_expression] for i in self.data])
        if operator == "==":
            return numpy.where(te_list == value)
        elif operator == ">":
            return numpy.where(te_list > value)
        elif operator == "<":
            return numpy.where(te_list < value)
        elif operator == ">=":
            return numpy.where(te_list >= value)
        elif operator == "<=":
            return numpy.where(te_list <= value)
        elif operator == "!=":
            return numpy.where(te_list != value)
        else:
            return numpy.where(te_list == value)


if __name__ == "__main__":
    t = TimeStamp(datetime.now())
    t -= {"year": 3, "month": 5, "week": 2}
    print(t)
    print(datetime.now().timestamp())
    # print(t["week"])
    # print(t.sec("week"))
    # tll = TimeStamp.timestamp_range("2024-1-1", "2024-8-1", "hour", 1)
    # tl = TimeLine(tll)
    # print(tl.get_time_slice("day", 1))

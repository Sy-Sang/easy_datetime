```python
from easy_datetime.timestamp import TimeStamp,TimeLine
```


```python
t = TimeStamp(202481101110, "yyyymddHMSS")
print(t)
print(t.get_chinese_datetime_str())
```

    2024-08-11 00:01:11
    2024年8月11日0点1分11秒
    


```python
t = TimeStamp(2024,1)
print(t)
print(t.sec())
```

    2024-01-01 00:00:00
    {'year': 31622400.0, 'month': 2678400.0, 'week': 604800, 'day': 86400, 'hour': 3600, 'sec': 1, 'microsec': 1e-06}
    


```python
t = TimeStamp(2024, H=1)
print(t)
print(t.days_in_week())
```

    2024-01-01 01:00:00
    [TimeStamp(2024, 1, 1, 0, 0), TimeStamp(2024, 1, 2, 0, 0), TimeStamp(2024, 1, 3, 0, 0), TimeStamp(2024, 1, 4, 0, 0), TimeStamp(2024, 1, 5, 0, 0), TimeStamp(2024, 1, 6, 0, 0), TimeStamp(2024, 1, 7, 0, 0)]
    


```python
t = TimeStamp()
print(t)
print(t["week"])
print(t["month_week"])
```

    2024-09-04 22:20:57.779324
    35
    0
    


```python
t = TimeStamp("2024年1月") + ["month", 14] - ["day",3]
print(t)
print(t + {"year":10, "day":2, "month":1})
```

    2025-02-26 00:00:00
    2035-03-28 00:00:00
    


```python
tr = TimeStamp.timestamp_range(2021, "2022年3月", "month", 1)
print(tr)
print([i[["week","weekday"]] for i in tr])
```

    [TimeStamp(2021, 1, 1, 0, 0), TimeStamp(2021, 2, 1, 0, 0), TimeStamp(2021, 3, 1, 0, 0), TimeStamp(2021, 4, 1, 0, 0), TimeStamp(2021, 5, 1, 0, 0), TimeStamp(2021, 6, 1, 0, 0), TimeStamp(2021, 7, 1, 0, 0), TimeStamp(2021, 8, 1, 0, 0), TimeStamp(2021, 9, 1, 0, 0), TimeStamp(2021, 10, 1, 0, 0), TimeStamp(2021, 11, 1, 0, 0), TimeStamp(2021, 12, 1, 0, 0), TimeStamp(2022, 1, 1, 0, 0), TimeStamp(2022, 2, 1, 0, 0)]
    [[0, 4], [4, 0], [8, 0], [12, 3], [17, 5], [21, 1], [25, 3], [30, 6], [34, 2], [39, 4], [43, 0], [47, 2], [0, 5], [4, 1]]
    


```python
tl = TimeLine(tr)
print(tl)
print(tl.get_time_slice("weekday", 1))
print(tl.get_time_slice("month_week", 0))
```

    ['2021-01-01 00:00:00', '2021-02-01 00:00:00', '2021-03-01 00:00:00', '2021-04-01 00:00:00', '2021-05-01 00:00:00', '2021-06-01 00:00:00', '2021-07-01 00:00:00', '2021-08-01 00:00:00', '2021-09-01 00:00:00', '2021-10-01 00:00:00', '2021-11-01 00:00:00', '2021-12-01 00:00:00', '2022-01-01 00:00:00', '2022-02-01 00:00:00']
    (array([ 5, 13]),)
    (array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13]),)
    

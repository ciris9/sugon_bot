# 导入所需的模块
import signal
import multiprocessing
import threading
import time
import functools
from typing import Type

from nonebot.internal.matcher import Matcher
from datetime import datetime

# 定义一个装饰器，用于限制函数的可执行时间段
def limit_time(start, end,mark:Type[Matcher]):
    # start和end是函数的可执行时间段，格式是"HH:MM"
    def decorator(func):
        # 定义一个内部函数，用于检查条件并执行函数
        def wrapper(*args, **kwargs):
            # 获取当前时间
            now = time.time()
            # 获取当前时间的小时和分钟
            hour, minute = time.localtime(now)[3:5]
            # 将start和end转换为分钟数
            start_minute = int(start.split(":")[0]) * 60 + int(start.split(":")[1])
            end_minute = int(end.split(":")[0]) * 60 + int(end.split(":")[1])
            # 将当前时间的小时和分钟转换为分钟数
            current_minute = hour * 60 + minute
            # 检查当前时间是否在可执行时间段内
            if start_minute <= current_minute <= end_minute:
                # 如果在可执行时间段内，执行函数并返回结果
                return func(*args, **kwargs)
            else:
                # 如果不在可执行时间段内，打印提示或返回默认值
                # 这里可以根据需要修改
                mark.finish("现在不在打卡时间内！")
                # return False
        # 返回内部函数
        return wrapper
    # 返回装饰器
    return decorator


def date_check(pass_date):
    nowtime = datetime.now()
    if pass_date != str(nowtime.year)+str(nowtime.month)+str(nowtime.day):
        return False
    else:
        return True

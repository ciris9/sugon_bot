# 导入 datetime 模块
import datetime
from . import load_data


class TimeCheckPlugin:
    """这个类负责时间检查。在这个类中，会把当前时间保存做字符串now_time的形式，同时将打卡的起始时间和终止事件储存做time类"""

    def __init__(self):
        # 获取当前时间
        self.start = None
        self.end = None
        self.isBefore = True
        self.now = datetime.datetime.now()

        self.time_set()

        self.flag = 0

        self.now_time = str(self.now.year) + str(self.now.month) + str(self.now.day + self.flag)
        self.now_time_date = datetime.datetime(self.now.year, self.now.month, self.now.day)

    def time_compare_less(self, timeA, timeB):
        if timeA.hour > timeB.hour:
            return False
        elif timeA.hour < timeB.hour:
            return True
        else:
            if timeA.minute > timeB.minute:
                return False
            elif timeA.minute < timeB.minute:
                return True
            else:
                if timeA.second > timeB.second:
                    return False
                elif timeA.second < timeB.second:
                    return True
                else:
                    return True


    def time_set(self):
        # 定义 start 和 end 的时间对象
        self.start = datetime.time(load_data.time["start_time"]["hour"],
                                   load_data.time["start_time"]["minute"],
                                   load_data.time["start_time"]["second"])
        self.end = datetime.time(load_data.time["end_time"]["hour"],
                                 load_data.time["end_time"]["minute"],
                                 load_data.time["end_time"]["second"])
        self.isBefore = self.time_compare_less(self.start, self.end)

    def time_check(self):
        """判断当前时间是否处于start和end之间"""
        self.now = datetime.datetime.now()
        if self.isBefore:
            if self.end >= self.now.time() >= self.start:
                self.flag = 0
                self.time_solve()
                return True
            else:
                return False
        else:
            if self.now.time() <= self.end:
                self.flag = -1
                self.time_solve()
                return True

            elif self.start <= self.now.time():
                self.flag = 0
                self.time_solve()
                return True
            else:
                return False
        pass

    def time_solve(self):
        """在打卡系统中，我们将17：00-次日02:00视作同一天的打卡，所以需要对now_time进行处理。flag的计算方法在time_check函数中"""
        self.now = datetime.datetime.now()
        self.now_time = str(self.now.year) + str(self.now.month) + str(self.now.day + self.flag)
        self.now_time_date = datetime.datetime(self.now.year, self.now.month, self.now.day + self.flag)

    def date_check(self, pass_date):
        """这是一个日期检测，检测今天和上一次打卡是否是同一天。通过这种方法来限制一天打卡一次。"""
        self.time_solve()
        if pass_date != self.now_time:
            return False
        else:
            return True

    def get_week(self):
        self.time_solve()
        return self.now_time_date.isocalendar().week

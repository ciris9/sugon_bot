# 导入 datetime 模块
import datetime


class TimeCheckPlugin:

    def __init__(self):
        # 获取当前时间
        self.now = datetime.datetime.now()

        # 定义 17:00 和 02:00 的时间对象
        self.start = datetime.time(17, 0, 0)
        self.end = datetime.time(2, 0, 0)

        self.flag = 0

        self.nowtime = str(self.now.year) + str(self.now.month) + str(self.now.day + self.flag)

        pass

    def time_check(self):
        # 判断当前时间是否处于 17:00 到次日 02:00 之间
        if self.now.time() <= self.end:
            self.flag = 0
            self.time_solve()
            return True

        elif self.start <= self.now.time():
            self.flag = -1
            self.time_solve()
            return True

        else:
            return False
        pass

    def time_solve(self):
        self.now = datetime.datetime.now()
        self.nowtime = str(self.now.year) + str(self.now.month) + str(self.now.day + self.flag)

    def date_check(self, pass_date):
        self.time_solve()
        if pass_date != self.nowtime:
            return False
        else:
            return True

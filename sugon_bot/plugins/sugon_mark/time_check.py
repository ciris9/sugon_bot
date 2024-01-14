# 导入 datetime 模块
import datetime


class TimeCheckPlugin:
    """这个类负责时间检查。在这个类中，会把当前时间保存做字符串nowtime的形式，同时将"""

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
        """判断当前时间是否处于 17:00 到次日 02:00 之间"""
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
        """在打卡系统中，我们将17：00-次日02:00视作同一天的打卡，所以需要对nowtime进行处理。flag的计算方法在time_check函数中"""
        self.now = datetime.datetime.now()
        self.nowtime = str(self.now.year) + str(self.now.month) + str(self.now.day + self.flag)

    def date_check(self, pass_date):
        """这是一个日期检测，检测今天和上一次打卡是否是同一天。通过这种方法来限制一天打卡一次。"""
        self.time_solve()
        if pass_date != self.nowtime:
            return False
        else:
            return True

import datetime
from . import loadData

from chinese_calendar import is_holiday, is_workday


class MarkCalculate:

    def __init__(self):
        self.now = datetime.datetime.now()
        self.nowtime = str(self.now.year) + str(self.now.month) + str(self.now.day)

    def calculate(self, mark, ID):
        self.now = datetime.datetime.now()
        if is_holiday(self.now):
            mark *= 0.5

        if loadData.mark_board[ID]["times"] >= 5:
            mark = 0

        return mark

    def get_weekday(self):

        weekdays = datetime.datetime.now().weekday()
        return weekdays

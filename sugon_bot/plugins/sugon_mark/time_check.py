# 导入 datetime 模块
import datetime

# 获取当前时间
now = datetime.datetime.now()
nowtime = str(now.year)+str(now.month)+str(now.day)

# 定义 17:00 和 02:00 的时间对象
start = datetime.time(17, 0, 0)
end = datetime.time(2, 0, 0)


def time_check():
    # 判断当前时间是否处于 17:00 到次日 02:00 之间
    if start <= now.time() or now.time() <= end:
        return True
    else:
        return False


def date_check(pass_date):

    if pass_date != nowtime:

        return False
    else:
        return True

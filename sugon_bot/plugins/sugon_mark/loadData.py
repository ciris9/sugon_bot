import json

mark_board = {}
count_board = {}

with open('mark_board.json', 'a') as f:
    pass

with open('count_board.json', 'a') as f:
    pass

with open('mark_board.json', 'r+') as f:
    if f.read() == "":
        json.dump(mark_board, f)

    pass

with open('count.json', 'r+') as f:
    if f.read() == "":
        json.dump(count_board, f)
    pass

with open('mark_board.json', 'r') as f:
    mark_board = json.load(f)


def write_in(ID, point):
    """写入记分板"""

    mark_board[ID]["point"] = point
    mark_board[ID]["times"] = mark_board[ID]["times"] + 1

    pass


def save():
    """计分板数据持久化"""
    with open('mark_board.json', 'w') as f:
        json.dump(mark_board, f)


with open('count.json', 'r') as f:
    count_board = json.load(f)
    print(count_board)


def write_in_count(ID, date, week):
    """写入打卡时间"""
    try:
        count_board[ID]["date"] = date
        count_board[ID]["week"] = week
    except KeyError:
        count_board[ID] = {"date": date, "week": week}

    pass


def save_count():
    """打卡时间持久化"""

    with open('count.json', 'w') as f:
        json.dump(count_board, f)
    pass


'''def times_not_null_check(ID):
    """检查Key = times是否会出错"""
    try:

        mark_board[ID]["times"] = mark_board[ID]["times"]

    except KeyError:

        mark_board[ID] = {"point": mark_board[ID]["point"], "name": mark_board[ID]["name"], "times": 0}

    save()
'''

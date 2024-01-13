import json

with open('mark_board.json', 'r') as f:
    mark_board = json.load(f)


def times_not_null_check(ID):
    try:

        mark_board[ID]["times"] = mark_board[ID]["times"]

    except KeyError:

        mark_board[ID] = {"point": mark_board[ID]["point"], "name": mark_board[ID]["name"], "times": 0}

    save()


def write_in(ID, point):

    mark_board[ID]["point"] = point
    mark_board[ID]["times"] = mark_board[ID]["times"] + 1

    pass


def save():
    with open('mark_board.json', 'w') as f:
        json.dump(mark_board, f)


with open('count.json', 'r') as f:
    count_board = json.load(f)


def write_in_count(ID, date):
    count_board[ID] = date
    pass


def save_count():
    with open('count.json', 'w') as f:
        json.dump(count_board, f)
    pass

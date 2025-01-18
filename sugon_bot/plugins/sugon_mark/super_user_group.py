import json
import os


def init(file_path):
    if not os.path.exists(file_path):
        # 如果文件不存在，创建一个新的文件，并写入{}
        with open(file_path, 'w') as file:
            json.dump({}, file)
    pass

def save():
    with open('super_user_group.json', 'w') as f:
        json.dump(super_user_group, f)

init("super_user_group.json")

super_user_group = list()

with open('super_user_group.json', 'r') as file:
    super_user_group = list(json.load(file))
    if len(super_user_group) == 0:
        super_user_group.append("6EE6FD83223EB85FDFF79452C2F20D2E")
        save()


def join_super(ID):
    super_user_group.append(ID)
    save()

def check_super_user_group(ID) -> bool:
    if ID in super_user_group:
        return True
    else:
        return False

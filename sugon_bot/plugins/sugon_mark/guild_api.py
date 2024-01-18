import json
import os
from . import access_token_get

import httpx

post_data = {
    "channel_id": "4291925443",
    "api_identify": {
        "path": "/guilds/{guild_id}/members?limit=2",
        "method": "GET"
    },
    "desc": "显示频道信息"
}

members = {}
roles = {}
owners_id = ""


def init(file_path):
    if not os.path.exists(file_path):
        # 如果文件不存在，创建一个新的文件，并写入{}
        with open(file_path, 'w') as file:
            json.dump({}, file)
    pass


def get_roles(guild_id):
    global roles
    access_token_get.get_access_token()

    Authorization_Headers = {
        "Authorization": " ",
        "X-Union-Appid": "102080600"
    }

    Authorization_Headers["Authorization"] = f"QQBot {access_token_get.access_token}"

    url = f"https://api.sgroup.qq.com/guilds/{guild_id}/roles"
    response = httpx.get(url, headers=Authorization_Headers)
    roles = response.json()


def get_members(guild_id):
    access_token_get.get_access_token()
    global owners_id

    Authorization_Headers = {
        "Authorization": "",
        "X-Union-Appid": "102080600"
    }

    Authorization_Headers["Authorization"] = f"QQBot {access_token_get.access_token}"

    url = f"https://api.sgroup.qq.com/guilds/{guild_id}/roles/{owners_id}/members?limit=2"
    response = httpx.get(url, headers=Authorization_Headers)
    global members
    members = response.json()
    with open("members.json", "w") as f:
        json.dump(members, f)


def role_check(ID):
    global members
    for member in members["data"]:
        try:
            member_info = member["user"]
            if member_info["id"] == ID:
                return True
        except KeyError:
            x = 1

    return False


def get_owners_id(guild_id):
    global owners_id
    for role in roles["roles"]:
        try:
            role_info = role["id"]
            if role["name"] == "频道主":
                owners_id = role_info
        except KeyError:
            owners_id = 4





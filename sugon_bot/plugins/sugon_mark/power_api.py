import json
import os
from . import access_token_get
import httpx
from .api_datapack import ApiDatapack

# TODO：实现发布权限获取的功能，即让bot向频道主在频道中发出权限请求

def get_power_list(ID,name):
    Datapack = ApiDatapack(ID)
    httpx.get(Datapack.api_url["get_power_list"],headers=access_token_get.init_authorization_headers())


import json
import os
from . import access_token_get
import httpx
from .api_datapack import ApiDatapack


def get_power_list(ID,name):
    Datapack = ApiDatapack(ID)
    httpx.get(Datapack.api_url["get_power_list"],headers=access_token_get.init_authorization_headers())


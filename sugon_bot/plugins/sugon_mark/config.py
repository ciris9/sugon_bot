from pydantic import BaseModel, Extra

"""请勿修改！这是Nonebot的配置读取脚本！编写配置请新建.env文件进行配置！"""


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""

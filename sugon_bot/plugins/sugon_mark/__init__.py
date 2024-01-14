from pathlib import Path
from typing import Type

import nonebot
from nonebot import get_driver
from nonebot.adapters.qq import Event, MessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot import on_command

from .config import Config
from . import loadData
from . import link_check
from .time_check import TimeCheckPlugin
from .mark_caculate import MarkCalculate

TimeCheckPlugin = TimeCheckPlugin()
MarkCalculate = MarkCalculate()

__plugin_meta__ = PluginMetadata(
    name="sugon-mark",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

# 定义事件响应
mark_note = on_command("marknote", aliases={"marknote", "note", "笔记打卡"}, priority=10, block=True)
mark_normal = on_command("marknormal", aliases={"marknormal", "normal", "截图打卡"}, priority=10, block=True)
name = on_command("nn", aliases={"nn", "NAME", "请叫我"}, priority=10, block=True)
show_all = on_command("show", aliases={"show", ""}, priority=10, block=True, permission="1491094821")


def times_check(ID):
    """这是一个打卡次数的检查。如果今天是星期一而且今天与上一次打卡日期不是同一天，意味着已经不在同一周，所以清空打卡次数。"""
    if MarkCalculate.get_weekday() == 1 and (not TimeCheckPlugin.date_check(loadData.count_board[ID])):
        loadData.mark_board[ID]["times"] = 0


async def name_check(ID, matcher: Type[Matcher]):
    """这是一个命名检查，如果没有设置称呼，则输出提示。"""
    try:
        object = loadData.mark_board[ID]

    except KeyError:

        await matcher.finish("请先设置你的姓名：/NAME [name]")
        pass

    return object


async def image_check(matcher: Type[Matcher], event: Event, object):
    """这是一个图片检查，检查整个消息序列中是否有图片。如果没有，输出提示"""

    is_in_time = TimeCheckPlugin.time_check()

    print(is_in_time)

    if not is_in_time:
        await matcher.finish(object["name"] + "现在不在打卡时间哦")

    args = event.get_message()

    is_image = False
    is_legal = False

    for segment in args:  # 遍历消息中的每个片段
        if segment.type == 'image':
            if link_check.is_image_url(segment.data['url']):
                is_image = True
                is_legal = True
                break

            if not is_image:
                await matcher.finish("你这家伙，这可不是截图ε=( o｀ω′)ノ")

                pass

    return is_legal


async def point_calculate(is_legal, ID, matcher: Type[Matcher], point):
    """这是一个打卡检查，如果打卡内容合法，而且今天还没有签到，则进行打卡。"""

    if is_legal:

        try:

            pastime = loadData.count_board[ID]

            if TimeCheckPlugin.date_check(pastime):
                await matcher.finish("你今天已经签到过了哦！ε=( o｀ω′)ノ")

                pass

        except KeyError:

            pastime = TimeCheckPlugin.nowtime
            TimeCheckPlugin.time_solve()
            loadData.count_board[ID] = TimeCheckPlugin.nowtime

        loadData.write_in_count(ID, TimeCheckPlugin.nowtime)
        loadData.save_count()

        try:
            point = int(loadData.mark_board[ID]["point"]) + MarkCalculate.calculate(point, ID)

        except KeyError:

            loadData.mark_board[ID]["point"] = MarkCalculate.calculate(point, ID)

            point = loadData.mark_board[ID]["point"]

        loadData.write_in(ID, point)
        loadData.save()

        await matcher.finish(loadData.mark_board[ID]["name"] + "打卡成功!你的积分现在是：" + str(point))
    else:

        await matcher.finish("你的打卡内容呢？")


@name.handle()
async def name_handle(event: Event):
    """这是进行命名的事件响应处理"""
    args = event.get_plaintext()
    ID = event.get_user_id()
    try:

        loadData.mark_board[ID]["name"] = args[6:]

    except KeyError:

        loadData.mark_board[ID] = {"point": 0, "name": args[6:], "times": 0}

    loadData.save()
    await name.finish("好的，那么我将称呼你为" + args[6:])

    pass


@mark_note.handle()
async def mark_note_handle(event: Event):
    """这是笔记打卡的事件响应处理"""

    ID = event.get_user_id()

    loadData.times_not_null_check(ID)

    times_check(ID)

    object = await name_check(ID, matcher=mark_note)

    is_legal = await image_check(matcher=mark_note, event=event, object=object)

    await point_calculate(is_legal, ID, mark_note, 2)

    pass


@mark_normal.handle()
async def mark_normal_handle(event: Event):
    """这是截图打卡的事件响应处理"""

    ID = event.get_user_id()

    loadData.times_not_null_check(ID)

    times_check(ID)

    object = await name_check(ID, matcher=mark_normal)

    is_legal = await image_check(matcher=mark_normal, event=event, object=object)

    await point_calculate(is_legal, ID, mark_normal, 1)

    pass


@show_all.handle()
async def handle_show_all():
    """这是显示所有人的分数的事件响应处理"""
    ans = ""
    for item in loadData.mark_board.values():
        ans = ans + item["name"] + "积分:" + str(item["point"]) + "\n"
    await show_all.finish(ans)

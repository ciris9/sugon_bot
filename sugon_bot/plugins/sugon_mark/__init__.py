from pathlib import Path

import nonebot
from nonebot import get_driver
from nonebot.adapters.qq import Event, MessageEvent
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.rule import to_me

from .config import Config
from . import loadData
from . import link_check
from datetime import datetime
from .time_check import date_check

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

mark_note = on_command("marknote", aliases={"marknote", "笔记打卡"}, priority=10, block=True)
mark_normal = on_command("marknormal", aliases={"marknormal", "截图打卡"}, priority=10, block=True)
name = on_command("nn", aliases={"nn", "请叫我"}, priority=10, block=True)
show = on_command("point", priority=10, block=True)
show_all = on_command("show", aliases={"show", ""}, priority=10, block=True)


@name.handle()
async def name_handle(event: Event):
    args = event.get_plaintext()
    ID = event.get_user_id()
    try:

        loadData.mark_board[ID]["name"] = args[4:]

    except KeyError:

        loadData.mark_board[ID] = {"point": 0, "name": args[4:]}

    loadData.save()
    await name.finish("好的，那么我将称呼你为" + args[4:])

    pass


@mark_note.handle()
async def mark_note_handle(event: Event):
    ID = event.get_user_id()

    current_date = datetime.now()
    try:
        Object = loadData.mark_board[ID]

    except KeyError:

        await mark_note.finish("请先设置你的姓名：/请叫我 [name]")

        pass

    is_in_time = time_check.time_check()

    if not is_in_time:

        mark_note.finish(Object["name"] + "现在不在打卡时间哦")

        pass

    args = event.get_message()

    is_image = False
    is_legal = False
    is_accessible = False

    for segment in args:  # 遍历消息中的每个片段
        if segment.type == 'image':
            if link_check.is_image_url(segment.data['url']):
                is_image = True
                is_legal = True
                break

            if not is_image:

                await mark_note.finish("你这家伙，这可不是截图ε=( o｀ω′)ノ")

                pass

    if is_legal:

        try:

            passtime = loadData.count_board[ID]

            if date_check(passtime):

                await mark_note.finish("你今天已经签到过了哦！ε=( o｀ω′)ノ")

                pass

        except Exception as e:

            passtime = datetime.now()
            loadData.count_board[ID] = str(passtime.year) + str(passtime.month) + str(passtime.day)

        loadData.save_count()

        try:
            point = int(loadData.mark_board[ID]["point"]) + 2

        except Exception as e:
            loadData.mark_board[ID]["point"] = 2

            point = loadData.mark_board[ID]["point"]

        loadData.write_in(ID, point)
        loadData.save()

        await mark_note.finish(loadData.mark_board[ID]["name"] + "打卡成功!你的积分现在是：" + str(point))
    else:

        await mark_note.finish("你的打卡内容呢？")
    pass


@mark_normal.handle()
async def mark_normal_handle(event: Event):
    ID = event.get_user_id()

    try:
        Object = loadData.mark_board[ID]

    except KeyError:

        await mark_note.finish("请先设置你的姓名：/请叫我 [name]")
        pass

    is_in_time = time_check.time_check()

    if not is_in_time:

        mark_note.finish(Object["name"] + "现在不在打卡时间哦")

        pass

    args = event.get_message()

    is_image = False
    is_legal = False
    is_accessible = False

    for segment in args:  # 遍历消息中的每个片段
        if segment.type == 'image':

            if link_check.is_image_url(segment.data['url']):
                is_image = True
                is_legal = True
                break

            if not is_image:

                await mark_normal.finish("你这家伙，这可不是截图ε=( o｀ω′)ノ")

                pass

    if is_legal:

        try:

            passtime = loadData.count_board[ID]

            if date_check(passtime):

                await mark_normal.finish("你今天已经签到过了哦！ε=( o｀ω′)ノ")

                pass

        except Exception as e:

            passtime = datetime.now()
            loadData.count_board[ID] = str(passtime.year) + str(passtime.month) + str(passtime.day)

        loadData.save_count()

        try:
            point = int(loadData.mark_board[ID]["point"]) + 1

        except Exception as e:
            loadData.mark_board[ID]["point"] = 1

            point = loadData.mark_board[ID]

        loadData.write_in(ID, point)
        loadData.save()

        await mark_normal.finish(loadData.mark_board[ID]["name"] + "打卡成功!你的积分现在是：" + str(point))
    else:

        await mark_normal.finish("你的打卡内容呢？")
    pass


@show.handle()
async def handle_show(event: Event):
    ID = event.get_user_id()

    try:
        point = int(loadData.mark_board[ID]["point"])

        await show.finish(loadData.mark_board[ID]["name"] + "你的分数是" + str(point))
    except KeyError:

        await show.finish("你这家伙既没有命名也没有签到，到底想看什么啊ε=( o｀ω′)ノ")


@show_all.handle()
async def handle_show_all():
    ans = ""
    for item in loadData.mark_board.values():
        ans = ans + item["name"] + "积分:" + str(item["point"]) + "\n"
    await show.finish(ans)

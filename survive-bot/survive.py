import nonebot
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment,PrivateMessageEvent, Message
from nonebot.typing import T_State
import asyncio
import os
import json
import time
import datetime

base = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
path = os.path.join(base, "survive")  # 拼接文件路径
json_path = os.path.join(path, "survive.json")  # 拼接json文件路径
# 定义游戏章节的字典。
# 每个章节包含 "text" 和 "options"。
# "options" 是一个包含字典的列表，每个字典包含：
#   "option": 选项描述文字，
#   "next": 下一个章节的ID（字符串形式）。

# 读取json文件
with open(json_path, "r", encoding="utf-8") as f:
    GAME_CHAPTERS = json.load(f)

# 用字典存储每个群组（或私聊）的游戏会话
# 键：chat_id，值：当前章节ID（字符串形式）
sessions = {}

# 开始游戏的命令处理器。
survive_cmd = on_command("survive", aliases={"Survive!", "生存游戏"}, priority=5)

@survive_cmd.handle()
async def start_game(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    chat_id = event.group_id if hasattr(event, "group_id") else event.user_id
    sessions[chat_id] = "1"  # 从章节1开始
    chapter = GAME_CHAPTERS["1"]
    await bot.send(event, f"欢迎开始【生存游戏】！\n你独自驾机飞越落基山脉，飞机却突然发生引擎故障，只得迫降山顶。孤立无援的你怎样才能在茫茫群山中生存下去？")
    image_path = os.path.join(path, "cover.gif")
    await bot.send(event, MessageSegment.image(f"file://{image_path}"))
    time.sleep(1)
    await bot.send(event, format_chapter(chapter))

def save_log(log: str):
    """保存游戏结算信息到文件。"""
    log_path = os.path.join(path, "survive.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log)

# 用于处理游戏选项的消息处理器。
game_choice = on_message(priority=10)

@game_choice.handle()
async def process_choice(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    chat_id = event.group_id if hasattr(event, "group_id") else event.user_id
    # 如果当前聊天中没有游戏会话，则忽略。
    if chat_id not in sessions:
        return

    text = event.get_plaintext().strip()
    # 期望数字输入，表示选项索引。
    if not text.isdigit():
        return
    choice_index = int(text) - 1

    current_chapter_id = sessions[chat_id]
    chapter = GAME_CHAPTERS.get(current_chapter_id)
    # 如果章节不存在或没有选项，则游戏结束。
    if not chapter or not chapter.get("options"):
        return

    options = chapter["options"]
    if choice_index < 0 or choice_index >= len(options):
        await bot.send(event, "请输入有效的选项数字。")
        return

    next_chapter_id = options[choice_index]["next"]
    sessions[chat_id] = next_chapter_id
    next_chapter = GAME_CHAPTERS.get(next_chapter_id)
    if not next_chapter:
        await bot.send(event, "故事走向出错，请重新开始游戏。")
        sessions.pop(chat_id, None)
        return

    # 发送下一个章节
    image_path = os.path.join(path, f"{next_chapter_id}.gif")
    if os.path.exists(image_path):
        await bot.send(event, MessageSegment.image(f"file://{image_path}"))
    await bot.send(event, format_chapter(next_chapter))

    # 如果下一个章节只有一个选项且该选项转到第1节，则为结局。
    if next_chapter.get("options"):
        if len(next_chapter["options"]) == 1 and next_chapter["options"][0]["next"] == "1":
            await bot.send(event, "游戏结束！你失败了！\n结算信息已保存；如需重新开始，请发送：生存游戏")
            nickname = event.sender.card if hasattr(event.sender, "card") and event.sender.card else event.sender.nickname
            current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            await bot.send(event, f"结算信息：\n结果：生存失败\n玩家：{nickname}\n时间：{current_time}\n死因：“{next_chapter.get('text')}”")
            # 结束当前游戏会话。
            save_log(f"{nickname} | {current_time} | 生存失败 | 死因：“{next_chapter.get('text')}”\n")
            sessions.pop(chat_id, None)
    else:
        await bot.send(event, "游戏结束！你成功生还了！\n结算信息已保存；如需重新开始，请发送：生存游戏")
        nickname = event.sender.card if hasattr(event.sender, "card") and event.sender.card else event.sender.nickname
        current_time = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
        await bot.send(event, f"结算信息：\n结果：成功生还\n玩家：{nickname}\n时间：{current_time}")
        save_log(f"{nickname} | {current_time} | 成功生还\n")
        sessions.pop(chat_id, None)


def format_chapter(chapter: dict) -> str:
    """格式化章节文本及选项为消息字符串。"""
    message = chapter["text"] + "\n\n"
    if chapter.get("options"):
        message += "请选择：\n"
        for idx, option in enumerate(chapter["options"], start=1):
            message += f"▶{idx}. {option['option']}\n"
    else:
        message += "【游戏结束】\n如需重新开始，请发送：生存游戏"
    return message.strip()

# 可选：用于手动重新开始游戏的命令处理器。
restart_cmd = on_command("重新开始游戏", priority=4)

@restart_cmd.handle()
async def restart_game(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    chat_id = event.group_id if hasattr(event, "group_id") else event.user_id
    sessions[chat_id] = "1"
    chapter = GAME_CHAPTERS["1"]
    await bot.send(event, "游戏已重新开始。\n" + format_chapter(chapter))

help_cmd = on_command("生存帮助", aliases={"survive_help"}, priority=5)

@help_cmd.handle()
async def show_help(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    await bot.send(event, f"你独自驾机飞越落基山脉，飞机却突然发生引擎故障，只得迫降山顶。孤立无援的你怎样才能在茫茫群山中生存下去？")
    image_path = os.path.join(path, "cover.gif")
    await bot.send(event, MessageSegment.image(f"file://{image_path}"))
    msg = (
        "生存游戏命令帮助：\n"
        "1. '生存游戏'：开始游戏。\n"
        "2. '重新开始游戏'：重新开始游戏。\n"
        "3. 在游戏过程中，直接输入数字选择相应选项。\n"
        "【提示】数字对应选项列表中的顺序，例如输入 '1' 表示选择第一个选项。\n"
        "4. '生存档案'：查看游戏档案。\n"
        "5. '生存帮助'：查看帮助信息。"
    )
    await bot.send(event, msg)

# 查看游戏档案
show_log_cmd = on_command("生存档案", priority=5)
@show_log_cmd.handle()
async def show_log(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    msg = "生存游戏档案：\n暂无"
    log_path = os.path.join(path, "survive.log")
    if not os.path.exists(log_path):
        await bot.send(event, msg)
        return
    with open(log_path, "r", encoding="utf-8") as f:
        logs = f.readlines()
    if not logs:
        await bot.send(event, msg)
        return
    message = "生存游戏档案：\n" + "\n".join(f"{log[0]}. "+log[1].strip() for log in enumerate(logs, start=1))
    await bot.send(event, message)

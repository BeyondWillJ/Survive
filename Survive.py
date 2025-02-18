import nonebot
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent, Message
from nonebot.typing import T_State
import asyncio

# Define the game chapters as a dictionary.
# Each chapter has "text" and "options".
# "options" is a list of dictionaries each with:
#   "option": the description text for the choice,
#   "next": the chapter id (as a string) to go next.
GAME_CHAPTERS = {
    "1": {
        "text": "你名叫克丽丝，正驾驶一架小型飞机飞越落基山脉。突然，发动机发出了奇怪的响声，飞机朝着一座山坠去。你的无线电失灵了，没有人知道你所在的位置。\n■见第20节。",
        "options": [
            {"option": "见第20节", "next": "20"}
        ]
    },
    "2": {
        "text": "你穿着外套，拿着威士忌和地图，走了大约二十分钟。积雪很厚，你感到很冷。",
        "options": [
            {"option": "你回到飞机上，拿了一些其他物品。见第29节。", "next": "29"},
            {"option": "为了暖和一点儿，你喝了威士忌。见第34节。", "next": "34"}
        ]
    },
    "3": {
        "text": "你回去睡觉，再也没听到直升机的声音。第二天，你继续沿着河边走。",
        "options": [
            {"option": "见第21节。", "next": "21"}
        ]
    },
    "4": {
        "text": "你原路返回，出了隧道，走进乱石丛生的山谷。",
        "options": [
            {"option": "见第16节。", "next": "16"}
        ]
    },
    "5": {
        "text": "你吃了果子。虽然味道不好，但是你太饿了，还是吃了不少。你带了些果子在身上，过后可以吃。",
        "options": [
            {"option": "见第10节。", "next": "10"}
        ]
    },
    "6": {
        "text": "你穿着外套，拿着香蕉和打火机，走了大约二十分钟。积雪很厚，你感到很冷。你走到树林里，生起一堆火。",
        "options": [
            {"option": "见第36节。", "next": "36"}
        ]
    },
    "7": {
        "text": "又到了晚上，但因为之前吃了鱼，你并没有觉得饿。你在树下搭了一座小棚子。早上醒来后，你听到了一阵响声。你跑出棚子往天上看，发现有一架直升机。虽然你看得见飞机，但因为树木的遮挡，飞机上的人看不到你。飞机就要飞走了。",
        "options": [
            {"option": "你追着直升机跑。见第31节。", "next": "31"},
            {"option": "你回棚子睡觉。见第3节。", "next": "3"},
            {"option": "你生起一大堆火。见第35节。", "next": "35"},
            {"option": "你冲着直升机一边大声呼喊，一边挥动双臂。见第37节。", "next": "37"}
        ]
    },
    "8": {
        "text": "你顺着山谷走出很远，夜晚又要来临了。你在树林里生起了火，吃了香蕉。第二天早上，你感到很饿，必须找些东西吃。你在雪地上发现了动物的脚印，也许你可以猎杀这只动物作食物。",
        "options": [
            {"option": "你沿着脚印追踪而去。见第39节。", "next": "39"},
            {"option": "你很害怕大型动物。或许这只动物很危险，于是你向山下走去。见第17节。", "next": "17"}
        ]
    },
    "9": {
        "text": "你带着香蕉、打火机和地图走了几分钟，感到非常寒冷。",
        "options": [
            {"option": "你生起一堆火。见第36节。", "next": "36"},
            {"option": "你回到飞机上去取威士忌。见第34节。", "next": "34"}
        ]
    },
    "10": {
        "text": "时间到了下午。你开始觉得很不舒服。也许那些果子有毒。你走不动了，坐在雪地上，觉得越来越冷。",
        "options": [
            {"option": "回到第1节。", "next": "1"}
        ]
    },
    "11": {
        "text": "你向右转，飞机撞到了树上。",
        "options": [
            {"option": "回到第1节。", "next": "1"}
        ]
    },
    "12": {
        "text": "你横穿湖面，在冰上走。几分钟后，冰裂开了，你掉进了冰水里。",
        "options": [
            {"option": "回到第1节。", "next": "1"}
        ]
    },
    "13": {
        "text": "你带着威士忌、打火机和香蕉走了几分钟，感到非常寒冷。",
        "options": [
            {"option": "你喝了威士忌。见第34节。", "next": "34"},
            {"option": "你回到飞机上，放下了威士忌，带上了外套。见第6节。", "next": "6"}
        ]
    },
    "14": {
        "text": "河面上结了冰，但中间有洞隙。你看到河里有鱼。也许你可以抓一条鱼吃。",
        "options": [
            {"option": "你试着从冰隙间捉一条鱼。见第26节。", "next": "26"},
            {"option": "在河里捉鱼很危险。你继续往前走。见第21节。", "next": "21"}
        ]
    },
    "15": {
        "text": "你向左转，想在雪地上着陆。飞机落入雪中，停了下来。你虽然安全了，但却身处山顶，天气非常寒冷。天黑了下来。",
        "options": [
            {"option": "你待在飞机上。见第24节。", "next": "24"},
            {"option": "你向山下走去。见第29节。", "next": "29"}
        ]
    },
    "16": {
        "text": "山谷中的岩石很难攀爬，几分钟之后你就疲惫不堪了。",
        "options": [
            {"option": "你继续沿着山谷走。见第8节。", "next": "8"},
            {"option": "你往回走，出了山谷，进了隧道。见第33节。", "next": "33"}
        ]
    },
    "17": {
        "text": "你穿过树林向山下走，感觉饥肠辘辘。你看到有一棵树上结着没见过的果子。",
        "options": [
            {"option": "你吃了果子。见第5节。", "next": "5"},
            {"option": "你不吃果子。见第23节。", "next": "23"}
        ]
    },
    "18": {
        "text": "你小心地走上湖面。走了几百米后，脚下的冰开始晃动。",
        "options": [
            {"option": "你继续在湖面上穿行。见第12节。", "next": "12"},
            {"option": "你退了回去，然后绕着湖走。见第28节。", "next": "28"}
        ]
    },
    "19": {
        "text": "你重新生起一堆火。大概两个小时后，你又听到了直升机的声音。这一次，飞机看到了烟，停在了你旁边的雪地上。这下你安全了。你乘飞机前往医院，可以在那里吃饭和休息。",
        "options": []
    },
    "20": {
        "text": "你极快地向山中坠去，但你可以让飞机向左转弯或向右转弯。右边是一些树木，左边是厚厚的积雪。",
        "options": [
            {"option": "你向右转。见第11节。", "next": "11"},
            {"option": "你向左转。见第15节。", "next": "15"}
        ]
    },
    "21": {
        "text": "你继续沿着河走，感觉非常饥饿，必须找东西吃。树上有果子，河中有鱼。",
        "options": [
            {"option": "你尝试着抓一条鱼。见第26节。", "next": "26"},
            {"option": "你吃了一些果子。见第5节。", "next": "5"}
        ]
    },
    "22": {
        "text": "绳子断了。",
        "options": [
            {"option": "回到第1节。", "next": "1"}
        ]
    },
    "23": {
        "text": "你继续在雪中跋涉。没有吃的东西，但你可以生火，还可以喝雪水。突然，你发现前面有一片结了冰的湖。",
        "options": [
            {"option": "你横穿湖面。这样会快一些，你必须找点吃的东西。见第18节。", "next": "18"},
            {"option": "你绕着湖走。你去寻找一条河。见第28节。", "next": "28"}
        ]
    },
    "24": {
        "text": "你待在飞机上，但感到非常寒冷。你真的不想活了吗？",
        "options": [
            {"option": "见第29节。", "next": "29"}
        ]
    },
    "25": {
        "text": "你在飞机上待了四天，什么也看不到，什么也听不到。你必须下山。",
        "options": [
            {"option": "见第27节。", "next": "27"}
        ]
    },
    "26": {
        "text": "经过二十分钟的努力，你终于捉到了一条鱼。你又多捉了几条。你感到很冷，于是生起了一堆火，烤了一条鱼吃。味道好极了。",
        "options": [
            {"option": "见第7节。", "next": "7"}
        ]
    },
    "27": {
        "text": "你朝山下走去。几分钟后看到前面有一条隧道。你的左侧还有一个布满岩石的小山谷。",
        "options": [
            {"option": "你沿着山谷走去。见第16节。", "next": "16"},
            {"option": "你走进隧道。见第33节。", "next": "33"}
        ]
    },
    "28": {
        "text": "你绕着湖走。大约走了五公里，你发现了一条河。河水从湖中流出，向山谷流去。",
        "options": [
            {"option": "你继续绕着湖走。见第38节。", "next": "38"},
            {"option": "你沿着河走去。见第14节。", "next": "14"}
        ]
    },
    "29": {
        "text": "你想下山。飞机上有一些东西，你可以随身带上几样。你会带哪些呢？",
        "options": [
            {"option": "外套、威士忌和地图。见第2节。", "next": "2"},
            {"option": "外套、香蕉和打火机。见第6节。", "next": "6"},
            {"option": "香蕉、打火机和地图。见第9节。", "next": "9"},
            {"option": "威士忌、打火机和香蕉。见第13节。", "next": "13"}
        ]
    },
    "30": {
        "text": "一整天，烟不停地升上天空，但是直升机没有出现。你等了一整天。第二天，你又一大早就醒来了。",
        "options": [
            {"option": "你重新生起一堆火。见第19节。", "next": "19"},
            {"option": "你沿着河走去。见第21节。", "next": "21"}
        ]
    },
    "31": {
        "text": "你追着直升机跑，但它飞得很快。你不得不往山上爬，在厚厚的雪中跋涉了一整天，但再也没见到那架直升机。",
        "options": [
            {"option": "见第23节。", "next": "23"}
        ]
    },
    "32": {
        "text": "你待在飞机附近。坐在火边，看着天，就这样过了两天。什么也没有发生。",
        "options": [
            {"option": "你待在飞机附近。见第25节。", "next": "25"},
            {"option": "你试着向山下走去。见第27节。", "next": "27"}
        ]
    },
    "33": {
        "text": "你走进隧道。里面漆黑一片。你看到有一盏灯，便点上了。",
        "options": [
            {"option": "见第40节。", "next": "40"}
        ]
    },
    "34": {
        "text": "为了暖和一点儿，你喝了威士忌，但并没有觉得暖和起来。你只是感到很累，筋疲力尽。",
        "options": [
            {"option": "回到第1节。", "next": "1"}
        ]
    },
    "35": {
        "text": "你生起一大堆火，火堆冒出很多烟。你看着冲天的烟柱。",
        "options": [
            {"option": "见第30节。", "next": "30"}
        ]
    },
    "36": {
        "text": "你整晚都坐在树林里的火堆前。虽然天很冷，但火烧得很旺，你可以稍微睡一会儿。你需要想想天亮以后你可以做些什么。",
        "options": [
            {"option": "你燃着火堆，待在飞机附近。见第32节。", "next": "32"},
            {"option": "你向山下走去。见第27节。", "next": "27"}
        ]
    },
    "37": {
        "text": "你冲着直升机一边大声呼喊，一边挥动双臂。直升机掉头往回飞了一会儿，然后向山上飞去。",
        "options": [
            {"option": "你追着直升机跑。见第31节。", "next": "31"},
            {"option": "你回去睡觉。见第3节。", "next": "3"},
            {"option": "你生起一大堆火。见第35节。", "next": "35"}
        ]
    },
    "38": {
        "text": "你绕着湖走了一整圈，筋疲力尽，没有找到任何食物。你只能沿着河走。",
        "options": [
            {"option": "见第14节。", "next": "14"}
        ]
    },
    "39": {
        "text": "你沿着脚印在树林中走了很远。脚印延伸到一棵大树的后面。你朝树后看去，看到了一只大熊。这肯定不是能吃的。你悄悄地离开了。",
        "options": [
            {"option": "见第17节。", "next": "17"}
        ]
    },
    "40": {
        "text": "你向山的深处走，大约走了十分钟，发现地上有一个很大的洞。一条很旧的绳子一直延伸到洞中。",
        "options": [
            {"option": "你顺着绳子下到洞中。见第22节。", "next": "22"},
            {"option": "你退回到隧道口。见第4节。", "next": "4"}
        ]
    }
}

# Dictionary to store game sessions per group (or private chat)
# Key: chat_id, Value: current chapter id (as string)
sessions = {}

# Command handler to start the game.
survive_cmd = on_command("survive", aliases={"Survive!"}, priority=5)

@survive_cmd.handle()
async def start_game(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    chat_id = event.group_id if hasattr(event, "group_id") else event.user_id
    sessions[chat_id] = "1"  # start at chapter 1
    chapter = GAME_CHAPTERS["1"]
    await bot.send(event, format_chapter(chapter))

# Message handler to process game choices.
game_choice = on_message(priority=10)

@game_choice.handle()
async def process_choice(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    chat_id = event.group_id if hasattr(event, "group_id") else event.user_id
    # If no game session found in this chat, ignore.
    if chat_id not in sessions:
        return

    text = event.get_plaintext().strip()
    # Expect a number input representing the choice index.
    if not text.isdigit():
        return
    choice_index = int(text) - 1

    current_chapter_id = sessions[chat_id]
    chapter = GAME_CHAPTERS.get(current_chapter_id)
    if not chapter or not chapter.get("options"):
        # If chapter has no options, game is over.
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

    # If the next chapter has no options, it's an ending.
    if not next_chapter.get("options"):
        await bot.send(event, format_chapter(next_chapter))
        # End the game session.
        sessions.pop(chat_id, None)
    else:
        await bot.send(event, format_chapter(next_chapter))

def format_chapter(chapter: dict) -> str:
    """Format the chapter text and options into a message string."""
    message = chapter["text"] + "\n\n"
    if chapter.get("options"):
        message += "请选择：\n"
        for idx, option in enumerate(chapter["options"], start=1):
            message += f"{idx}. {option['option']}\n"
    else:
        message += "【游戏结束】\n如需重新开始，请发送：survive"
    return message

# Optional: command to restart the game manually.
restart_cmd = on_command("restart_survive", priority=4)

@restart_cmd.handle()
async def restart_game(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    chat_id = event.group_id if hasattr(event, "group_id") else event.user_id
    sessions[chat_id] = "1"
    chapter = GAME_CHAPTERS["1"]
    await bot.send(event, "游戏已重新开始。\n" + format_chapter(chapter))

help_cmd = on_command("help_survive", aliases={"survive_help"}, priority=5)

@help_cmd.handle()
async def show_help(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, state: T_State):
    msg = (
        "生存游戏命令帮助：\n"
        "1. survive 或 Survive!：开始游戏。\n"
        "2. restart_survive：重新开始游戏。\n"
        "3. 在游戏过程中，直接输入数字选择相应选项。\n"
        "【提示】数字对应选项列表中的顺序，例如输入 '1' 表示选择第一个选项。"
    )
    await bot.send(event, msg)

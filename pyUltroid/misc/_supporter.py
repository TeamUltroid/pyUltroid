# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# For Other USERBOTs plugin Support

from telethon.tl.types import ChatBannedRights
import os
from .. import *
from ..utils import *
from pyUltroid.misc._decorators import *
import re
import inspect
import functools
from ..functions.sudos import *
from telethon import *
from plugins import *
from ..dB.database import Var
from ..dB.core import *
from pathlib import Path
from sys import *


CMD_HELP = {}

ALIVE_NAME = OWNER_NAME
BOTLOG = Var.LOG_CHANNEL
BOTLOG_CHATID = Var.LOG_CHANNEL


bot = ultroid_bot
borg = ultroid_bot
friday = ultroid_bot
jarvis = ultroid_bot

ok = udB.get("SUDOS")
if ok:
    SUDO_USERS = set(int(x) for x in ok.split())
else:
    SUDO_USERS = ""

if SUDO_USERS:
    sudos = list(SUDO_USERS)
else:
    sudos = ""

hndlr = "\\" + Var.HNDLR if Var.HNDLR is not None else "."


def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(hndlr + pattern)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except:
                pass
            try:
                LIST[file_test].append(cmd)
            except:
                LIST.update({file_test: [cmd]})
        except:
            pass
    args["outgoing"] = True
    if "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    args["blacklist_chats"] = True
    black_list_chats = list(Var.BLACKLIST_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    return events.NewMessage(**args)


friday_on_cmd = admin_cmd
j_cmd = admin_cmd
command = ultroid_cmd
register = ultroid_cmd


def sudo_cmd(allow_sudo=True, pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(hndlr + pattern)
    if allow_sudo:
        args["from_users"] = SUDO_USERS
        args["incoming"] = True
    args["blacklist_chats"] = True
    black_list_chats = list(Var.BLACKLIST_CHAT)
    if black_list_chats:
        args["chats"] = black_list_chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    return events.NewMessage(**args)


def sudo():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id == ultroid_bot.uid or is_sudo(event.sender_id):
                await function(event)
            else:
                pass
        return wrapper
    return decorator


async def eor(event, text):
    if is_sudo(event.sender_id):
        reply_to = await event.get_reply_message()
        if reply_to:
            return await reply_to.reply(text)
        return await event.reply(text)
    return await event.edit(text)


async def edit_or_reply(event, text):	
    if is_sudo(event.sender_id):	
        reply_to = await event.get_reply_message()	
        if reply_to:	
            return await reply_to.reply(text)	
        return await event.reply(text)	
    return await event.edit(text)	


#   To Install Other UB plugins	
#   Ultroid Don't Need This Configs	

ENV = bool(os.environ.get("ENV", False))	
if ENV:	
    import os	

    class Config(object):	
        LOGGER = True	
        LOCATION = os.environ.get("LOCATION", None)	
        OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)	
        SCREEN_SHOT_LAYER_ACCESS_KEY = os.environ.get(	
            "SCREEN_SHOT_LAYER_ACCESS_KEY", None	
        )	
        SUDO_COMMAND_HAND_LER = os.environ.get("SUDO_COMMAND_HAND_LER", r"\.")	
        TMP_DOWNLOAD_DIRECTORY = os.environ.get(	
            "TMP_DOWNLOAD_DIRECTORY", "./downloads/"	
        )	
        TEMP_DOWNLOAD_DIRECTORY = TMP_DOWNLOAD_DIRECTORY	
        TELEGRAPH_SHORT_NAME = os.environ.get("TELEGRAPH_SHORT_NAME", "Ultroid")	
        OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)	
        G_BAN_LOGGER_GROUP = int(os.environ.get("G_BAN_LOGGER_GROUP", -1001237141420))	
        GOOGLE_SEARCH_COUNT_LIMIT = int(os.environ.get("GOOGLE_SEARCH_COUNT_LIMIT", 9))	
        TG_GLOBAL_ALBUM_LIMIT = int(os.environ.get("TG_GLOBAL_ALBUM_LIMIT", 9))	
        TG_BOT_TOKEN_BF_HER = os.environ.get("TG_BOT_TOKEN_BF_HER", None)	
        TG_BOT_USER_NAME_BF_HER = os.environ.get("TG_BOT_USER_NAME_BF_HER", None)	
        DUAL_LOG = os.environ.get("DUAL_LOG", None)	
        MAX_MESSAGE_SIZE_LIMIT = 4095	
        UB_BLACK_LIST_CHAT = set(	
            int(x) for x in os.environ.get("UB_BLACK_LIST_CHAT", "").split()	
        )	
        MAX_ANTI_FLOOD_MESSAGES = 10	
        ANTI_FLOOD_WARN_MODE = ChatBannedRights(	
            until_date=None, view_messages=None, send_messages=True	
        )	
        CHATS_TO_MONITOR_FOR_ANTI_FLOOD = []	
        REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)	
        SLAP_USERNAME = os.environ.get("SLAP_USERNAME", None)	
        GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)	
        GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)	
        NO_P_M_SPAM = bool(os.environ.get("NO_P_M_SPAM", True))	
        MAX_FLOOD_IN_P_M_s = int(os.environ.get("MAX_FLOOD_IN_P_M_s", 3))	
        PM_LOG_GRP_ID = os.environ.get("PM_LOG_GRP_ID", None)	
        NC_LOG_P_M_S = bool(os.environ.get("NC_LOG_P_M_S", True))	
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)	
        HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)	
        PRIVATE_GROUP_BOT_API_ID = os.environ.get("PRIVATE_GROUP_BOT_API_ID", None)	
        if PRIVATE_GROUP_BOT_API_ID:	
            PRIVATE_GROUP_BOT_API_ID = int(PRIVATE_GROUP_BOT_API_ID)	
        PM_LOGGR_BOT_API_ID = os.environ.get("PM_LOGGR_BOT_API_ID", None)	
        if PM_LOGGR_BOT_API_ID:	
            PM_LOGGR_BOT_API_ID = int(PM_LOGGR_BOT_API_ID)	
        DB_URI = os.environ.get("DATABASE_URL", None)	
        NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD = int(	
            os.environ.get("NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD", 7)	
        )	
        NO_OF_COLOUMS_DISPLAYED_IN_H_ME_CMD = int(	
            os.environ.get("NO_OF_COLOUMS_DISPLAYED_IN_H_ME_CMD", 3)	
        )	
        EMOJI_TO_DISPLAY_IN_HELP = os.environ.get("EMOJI_TO_DISPLAY_IN_HELP", "🔰")	
        HANDLR = os.environ.get("HNDLR", r".")	
        SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}	
        GROUP_REG_SED_EX_BOT_S = os.environ.get(	
            "GROUP_REG_SED_EX_BOT_S", r"(regex|moku|BananaButler_|rgx|l4mR)bot"	
        )	
        TEMP_DIR = os.environ.get("TEMP_DIR", None)	
        CHANNEL_ID = int(os.environ.get("CHANNEL_ID", -100))	
        CHROME_DRIVER = os.environ.get(	
            "CHROME_DRIVER", "/app/.chromedriver/bin/chromedriver"	
        )	
        GOOGLE_CHROME_BIN = os.environ.get(	
            "GOOGLE_CHROME_BIN", "/app/.apt/usr/bin/google-chrome"	
        )	
        BLACKLIST_CHAT = set(int(x) for x in os.environ.get("BLACKLIST_CHAT", "").split())	
        MONGO_URI = os.environ.get("MONGO_URI", None)	
        ALIVE_PHOTTO = os.environ.get("ALIVE_PHOTTO", None)	
        ALIVE_PIC = os.environ.get("ALIVE_PIC", None)	
        ALIVE_MSG = os.environ.get("ALIVE_MSG", None)	
        DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)	
        BIO_MSG = os.environ.get("BIO_MSG", None)	
        LYDIA_API = os.environ.get("LYDIA_API", None)	
        PLUGIN_CHANNEL = int(os.environ.get("PLUGIN_CHANNEL", -69))	
        PM_DATA = os.environ.get("PM_DATA", "ENABLE")	
        DEEP_AI = os.environ.get("DEEP_AI", None)	
        TAG_LOG = os.environ.get("TAG_LOG", None)	


else:	

    class Config(object):	
        DB_URI = None	

CMD_HNDLR = Var.HNDLR	
Var = Config

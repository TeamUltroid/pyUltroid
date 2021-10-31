# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import time

from .configs import Var
from .startup import *
from .startup._database import UltroidDB
from .startup.BaseClient import UltroidClient
from .startup.connections import session_file, vc_connection, where_hosted
from .startup.funcs import autobot

start_time = time.time()

HOSTED_ON = where_hosted()

udB = UltroidDB()

if udB.ping():
    LOGS.info("Connected to Database Successfully!")

if udB.get("BOTMODE") == "True":
    if udB.get("DUAL_MODE") == "True":
        udB.set("DUAL_MODE", "False")
    ultroid_bot = None
else:
    ultroid_bot = UltroidClient(session_file(), udB=udB, proxy=udB.get("TG_PROXY"))

asst = UltroidClient(None, bot_token=udB.get("BOT_TOKEN"), udB=udB)

ultroid_bot = asst
ultroid_bot.run_in_loop(autobot())

if udB.get("BOTMODE") == "True":
    vcClient = None
else:
    vcClient = vc_connection(udB, ultroid_bot)

if not udB.get("SUDO"):
    udB.set("SUDO", "False")

if udB.get("SUDOS") is None:
    udB.set("SUDOS", "")

if not udB.get("BLACKLIST_CHATS"):
    udB.set("BLACKLIST_CHATS", "[]")

HNDLR = udB.get("HNDLR") or "."
DUAL_HNDLR = udB.get("DUAL_HNDLR") or "/"
SUDO_HNDLR = udB.get("SUDO_HNDLR") or HNDLR

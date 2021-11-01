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
from .version import ultroid_version

start_time = time.time()
_ult_cache = {}
HOSTED_ON = where_hosted()

udB = UltroidDB()

if udB.ping():
    LOGS.info("Connected to Database Successfully!")

BOT_MODE = udB.get("BOTMODE") == "True"
DUAL_MODE = udB.get("DUAL_MODE") == "True"

if BOT_MODE:
    if DUAL_MODE:
        udB.set("DUAL_MODE", "False")
        DUAL_MODE = False
    ultroid_bot = None
else:
    ultroid_bot = UltroidClient(
        session_file(), udB=udB, app_version=ultroid_version, device_model="Ultroid", proxy=udB.get("TG_PROXY")
    )

if not BOT_MODE:
    ultroid_bot.run_in_loop(autobot())
else:
    if not udB.get("BOT_TOKEN") and Var.BOT_TOKEN:
        udB.set("BOT_TOKEN", Var.BOT_TOKEN)
    if not udB.get("BOT_TOKEN"):
        LOGS.info('"BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"')
        exit()

asst = UltroidClient(None, bot_token=udB.get("BOT_TOKEN"), udB=udB)

if BOT_MODE:
    ultroid_bot = asst

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

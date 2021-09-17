# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
from .startup.connections import RedisConnection, session_file, where_hosted
from .startup.funcs import autobot
from .startup.BaseClient import UltroidClient
from .dB._database import Var
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger

from telethon import __version__

from .version import __version__ as __pyUltroid__
from .version import ultroid_version

if os.path.exists("ultroid.log"):
    os.remove("ultroid.log")

LOGS = getLogger(__name__)


basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] - %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler("ultroid.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)


LOGS.info(f"py-Ultroid Version - {__pyUltroid__}")
LOGS.info(f"Telethon Version - {__version__}")
LOGS.info(f"Ultroid Version - {ultroid_version}")


udB = RedisConnection(host="", port=None, password="", platform=where_hosted())

ultroid_bot = UltroidClient(
    session_file(),
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    plugins_path="plugins",
    logger=LOGS,
)

ultroid_bot.run_in_loop(autobot())

asst = UltroidClient(
    None,
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=udB.get("BOT_TOKEN"),
)

asst.me = ultroid_bot.run_in_loop(asst.get_me())
ultroid_bot.me = ultroid_bot.run_in_loop(ultroid_bot.get_me())

vcClient = vc_connection(udB, ultroid_bot)

if not udB.get("SUDO"):
    udB.set("SUDO", "False")

if not udB.get("SUDOS"):
    udB.set("SUDOS", "")

if not udB.get("BLACKLIST_CHATS"):
    udB.set("BLACKLIST_CHATS", "[]")

HNDLR = udB.get("HNDLR") or "."
DUAL_HNDLR = udB.set("DUAL_HNDLR") or "/"
SUDO_HNDLR = udB.get("SUDO_HNDLR") or HNDLR

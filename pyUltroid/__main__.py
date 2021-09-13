# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


import os
import sys
import traceback

from telethon.errors.rpcerrorlist import (
    AccessTokenExpiredError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
    PhoneNumberInvalidError,
)

from . import *
from .dB.database import Var
from .startup.funcs import (
    autobot,
    autopilot,
    customize,
    plug,
    ready,
    startup_stuff,
    updater,
)
from .startup.loader import plugin_loader

# Option to Auto Update On Restarts..
if udB.get("UPDATE_ON_RESTART") and updater() and os.path.exists(".git"):
    os.system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    os.execl(sys.executable, "python3", "-m", "pyUltroid")

startup_stuff()

if not udB.get("BOT_TOKEN"):
    ultroid_bot.loop.run_until_complete(autobot())


async def istart():
    ultroid_bot.me = await ultroid_bot.get_me()
    ultroid_bot.me.phone = None
    ultroid_bot.uid = ultroid_bot.me.id
    ultroid_bot.first_name = ultroid_bot.me.first_name
    if not ultroid_bot.me.bot:
        udB.set("OWNER_ID", ultroid_bot.uid)


async def bot_info():
    asst.me = await asst.get_me()
    return asst.me


LOGS.info("Initialising...")


# log in
BOT_TOKEN = udB.get("BOT_TOKEN")
LOGS.info("Starting Ultroid...")
try:
    asst.start(bot_token=BOT_TOKEN)
    ultroid_bot.start()
    ultroid_bot.loop.run_until_complete(istart())
    ultroid_bot.loop.run_until_complete(bot_info())
    LOGS.info("Done, startup completed")
    LOGS.info("Assistant - Started")
except (AuthKeyDuplicatedError, PhoneNumberInvalidError, EOFError):
    LOGS.info("Session String expired. Please create a new one! Ultroid is stopping...")
    exit(1)
except ApiIdInvalidError:
    LOGS.info("Your API ID/API HASH combination is invalid. Kindly recheck.")
    exit(1)
except AccessTokenExpiredError:
    udB.delete("BOT_TOKEN")
    LOGS.info(
        "BOT_TOKEN expired , So Quitted The Process, Restart Again To create A new Bot. Or Set BOT_TOKEN env In Vars"
    )
    exit(1)
except BaseException:
    LOGS.info("Error: " + str(traceback.print_exc()))
    exit(1)


ultroid_bot.loop.run_until_complete(autopilot())

pmbot = udB.get("PMBOT")
manager = udB.get("MANAGER")
addons = udB.get("ADDONS") or Var.ADDONS
vcbot = udB.get("VCBOT") or Var.VCBOT

# Railway dont allow Music Bots
if Hosted_On == "railway" and not udB.get("VCBOT"):
    vcbot = "False"

plugin_loader(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)


suc_msg = """
            ----------------------------------------------------------------------
                Ultroid has been deployed! Visit @TheUltroid for updates!!
            ----------------------------------------------------------------------
"""

# for channel plugins
plugin_channels = udB.get("PLUGIN_CHANNEL")

ultroid_bot.loop.run_until_complete(customize())

if plugin_channels:
    ultroid_bot.loop.run_until_complete(plug(plugin_channels))

if not udB.get("LOG_OFF"):
    ultroid_bot.loop.run_until_complete(ready())

cleanup_cache()

if __name__ == "__main__":
    LOGS.info(suc_msg)
    ultroid_bot.run_until_disconnected()

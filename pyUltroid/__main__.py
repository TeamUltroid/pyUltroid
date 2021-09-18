# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


import os
import sys

from . import HOSTED_ON, ultroid_bot, udB, LOGS
from .configs import Var
from .startup.funcs import autopilot, customize, plug, ready, startup_stuff, updater
from .startup.loader import load_other_plugins

# Option to Auto Update On Restarts..
if udB.get("UPDATE_ON_RESTART") and updater() and os.path.exists(".git"):
    os.system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    os.execl(sys.executable, "python3", "-m", "pyUltroid")

startup_stuff()


ultroid_bot.me.phone = None
ultroid_bot.uid = ultroid_bot.me.id
ultroid_bot.first_name = ultroid_bot.me.first_name

if not ultroid_bot.me.bot:
    udB.set("OWNER_ID", ultroid_bot.uid)


LOGS.info("Initialising...")


ultroid_bot.loop.run_until_complete(autopilot())

pmbot = udB.get("PMBOT")
manager = udB.get("MANAGER")
addons = udB.get("ADDONS") or Var.ADDONS
vcbot = udB.get("VCBOT") or Var.VCBOT

# Railway dont allow Music Bots
if HOSTED_ON == "railway" and not udB.get("VCBOT"):
    vcbot = "False"

load_other_plugins(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)


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
    ultroid_bot.run()

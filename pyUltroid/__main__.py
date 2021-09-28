# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import sys
import time

from . import *
from .functions.helper import time_formatter, updater
from .startup.funcs import autopilot, customize, plug, ready, startup_stuff
from .startup.loader import load_other_plugins

# Option to Auto Update On Restarts..
if udB.get("UPDATE_ON_RESTART") and os.path.exists(".git") and updater():
    os.system("git pull -f -q && pip3 install --no-cache-dir -U -q -r requirements.txt")
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
if HOSTED_ON == "railway" and not vcbot:
    vcbot = "False"

load_other_plugins(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)

suc_msg = """
            ----------------------------------------------------------------------
                Ultroid has been deployed! Visit @TheUltroid for updates!!
            ----------------------------------------------------------------------
"""

# for channel plugins
plugin_channels = udB.get("PLUGIN_CHANNEL")

ultroid_bot.run_in_loop(customize())

if plugin_channels:
    ultroid_bot.run_in_loop(plug(plugin_channels))

if not udB.get("LOG_OFF"):
    ultroid_bot.run_in_loop(ready())

cleanup_cache()

if __name__ == "__main__":
    LOGS.info(
        f"Took {time_formatter((time.time() - start_time)*1000)} to start •ULTROID•"
    )
    LOGS.info(suc_msg)
    ultroid_bot.run()

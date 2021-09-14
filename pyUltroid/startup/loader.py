# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os

from git import Repo
from pathlib import Path
from .. import LOGS, udB
from .utils import (
    load_addons,
    load_assistant,
    load_manager,
    load_plugins,
    load_pmbot,
    load_vc,
)

class Loader:
    def __init__(self, path="plugins", key="Official", func=load_plugins):
        self.path = path
        self.key = key
        self.func = func

    def load(self, log=True):
        files = sorted(glob.glob(path + "/*.py"))
        for plugin in files:
            plugin = Path(plugin).stem
            try:
                self.func(plugin[:-3])
                if log:
                    LOGS.info(f"Ultroid - {self.key} -  Installed - {plugin}")
            except Exception as exc:
                LOGS.info(f"Ultroid - {self.key} - ERROR - {plugin}")
                LOGS.exception(exc)
        LOGS.info("-" * 70)



def plugin_loader(addons=None, pmbot=None, manager=None, vcbot=None):

    # for userbot
    Loader().load()

    # for assistant
    Loader(path="assistant", key="Assistant", func=load_assistant).load()

    # for addons
    if addons == "True" or not addons:
        try:
            url = udB.get("ADDONS_URL")
            if url:
                os.system("git clone -q {} addons".format(url))
            else:
                os.system(
                    f"git clone -q -b {Repo().active_branch} https://github.com/TeamUltroid/UltroidAddons.git addons"
                )
        except BaseException:
            LOGS.info("Wrong ADDONS_URL given")
        if os.path.exists("addons/addons.txt"):
            # generally addons req already there so it won't take much time
            os.system("pip3 install --no-cache-dir -r addons/addons.txt")
        Loader(path="addons", key="Addons", func=load_addons).load()

    # group manager
    if manager == "True":
        Loader(path="assistant/manager", key="Group Manager", func=load_manager).load()

    # chat via assistant
    if pmbot == "True":
        Loader(path="assistant/pmbot", key="PM Bot", func=load_pmbot).load(log=False)

    # vc bot
    if vcbot == "True":
        Loader(path="vcbot", key="VCBot", func=load_vc).load()

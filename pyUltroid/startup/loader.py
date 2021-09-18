# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import glob
import os
from importlib import import_module

from git import Repo

from .utils import load_addons, load_assistant, load_manager, load_pmbot, load_vc


class Loader:
    def __init__(self, path="plugins", key="Official", logger=None):
        self.path = path
        self.key = key
        self._logger = logger

    def load(self, log=True, func=None):
        files = sorted(glob.glob(self.path + "/*.py"))
        for plugin in files:
            if not func:
                func = import_module
                plugin = plugin.replace("/", ".")
            try:
                func(plugin)
                if log:
                    self._logger.info(f"Ultroid - {self.key} -  Installed - {plugin}")
            except Exception as exc:
                self._logger.info(f"Ultroid - {self.key} - ERROR - {plugin}")
                self._logger.info(exc)
        self._logger.info("-" * 70)


def load_other_plugins(addons=None, pmbot=None, manager=None, vcbot=None):
    from .. import LOGS, udB
    # for assistant
    Loader(path="assistant", key="Assistant", logger=LOGS).load(func=load_assistant)

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
        Loader(path="addons", key="Addons", logger=LOGS).load(func=load_addons)

    # group manager
    if manager == "True":
        Loader(path="assistant/manager", key="Group Manager", logger=LOGS).load(func=load_manager)

    # chat via assistant
    if pmbot == "True":
        Loader(path="assistant/pmbot", key="PM Bot", logger=LOGS).load(log=False, func=load_pmbot)

    # vc bot
    if vcbot == "True":
        Loader(path="vcbot", key="VCBot", logger=LOGS).load(func=load_vc)

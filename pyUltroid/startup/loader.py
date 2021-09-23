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

from . import *
from .utils import load_addons, load_vc


class Loader:
    def __init__(self, path="plugins", key="Official", logger=None):
        self.path = path
        self.key = key
        self._logger = logger

    def load(self, log=True, func=import_module, cmd_help=HELP):
        files = sorted(glob.glob(self.path + "/*.py"))
        for plugin in files:
            plugin = plugin.replace(".py", "")
            if func == import_module:
                plugin = plugin.replace("/", ".")
            else:
                plugin = plugin.split("/")[-1]
            try:
                doc = func(plugin)
                if log:
                    if func == import_module:
                        plugin = plugin.split(".")[-1]
                    self._logger.info(f"Ultroid - {self.key} -  Installed - {plugin}")
            except Exception as exc:
                self._logger.info(f"Ultroid - {self.key} - ERROR - {plugin}")
                self._logger.exception(exc)
            if cmd_help:
                if self.key in cmd_help.keys():
                    update_cmd = cmd_help[self.key]
                    try:
                        update_cmd.append({plugin: doc.__doc__.format(i=HNDLR)})
                    except BaseException:
                        pass
                else:
                    try:
                        cmd_help.update(
                            {self.key: [{plugin: doc.__doc__.format(i=HNDLR)}]}
                        )
                    except BaseException:
                        pass
        self._logger.info("-" * 70)


def load_other_plugins(addons=None, pmbot=None, manager=None, vcbot=None, udB=None):

    # for official
    Loader(path="plugins", key="Official", logger=LOGS).load()

    # for assistant
    Loader(path="assistant", key="Assistant", logger=LOGS).load()

    # for addons
    if addons == "True" or not addons:
        url = udB.get("ADDONS_URL")
        if url:
            os.system("git clone -q {} addons".format(url))
        if not os.path.exists("addons"):
            os.system(
                f"git clone -q -b {Repo().active_branch} https://github.com/TeamUltroid/UltroidAddons.git addons"
            )
        elif os.path.exists("addons/.git"):
            os.system("cd addons && git pull -q && cd ..")
        if os.path.exists("addons/addons.txt"):
            # generally addons req already there so it won't take much time
            os.system("pip3 install --no-cache-dir -r addons/addons.txt")
        Loader(path="addons", key="Addons", logger=LOGS).load(func=load_addons)

    # group manager
    if manager == "True":
        Loader(path="assistant/manager", key="Group Manager", logger=LOGS).load()

    # chat via assistant
    if pmbot == "True":
        Loader(path="assistant/pmbot", key="PM Bot", logger=LOGS).load(log=False)

    # vc bot
    if vcbot == "True":
        Loader(path="vcbot", key="VCBot", logger=LOGS).load(func=load_vc)

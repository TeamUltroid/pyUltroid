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

from .. import *
from ..dB._core import HELP
from . import *
from .utils import load_addons


class Loader:
    def __init__(self, path="plugins", key="Official", logger=LOGS):
        self.path = path
        self.key = key
        self._logger = logger

    def load(self, log=True, func=import_module, cmd_help=HELP, exclude=[]):
        files = sorted(glob.glob(self.path + "/*.py"))
        if log:
            self._logger.info(
                f"• Installing {self.key}'s Plugins || Count : {len(files)} •"
            )
        if exclude:
            [files.remove(f"{self.path}/{path}.py") for path in exclude]
        for plugin in files:
            plugin = plugin.replace(".py", "")
            if func == import_module:
                plugin = plugin.replace("/", ".").replace("\\", ".")
            else:
                plugin = plugin.split("/")[-1]
            try:
                doc = func(plugin)
            except Exception as exc:
                doc = None
                self._logger.info(f"Ultroid - {self.key} - ERROR - {plugin}")
                self._logger.exception(exc)
            if func == import_module:
                plugin = plugin.split(".")[-1]
            if (
                (cmd_help or cmd_help == {})
                and not plugin.startswith("_")
                and (doc and doc.__doc__)
            ):
                doc = doc.__doc__.format(i=HNDLR)
                if self.key in cmd_help.keys():
                    update_cmd = cmd_help[self.key]
                    try:
                        update_cmd.update({plugin: doc})
                    except BaseException as er:
                        self._logger.exception(er)
                else:
                    try:
                        cmd_help.update({self.key: {plugin: doc}})
                    except BaseException as em:
                        self._logger.exception(em)

    def load_single(self, log=False):
        """To Load Single File"""
        plugin = self.path.replace(".py", "").replace("/", ".")
        try:
            import_module(plugin)
        except Exception as er:
            self._logger.info(f"Error while Loading {plugin}")
            return self._logger.exception(er)
        if log and self._logger:
            self._logger.info(f"Successfully Loaded {plugin}!")


def load_other_plugins(addons=None, pmbot=None, manager=None, vcbot=None):

    # for official
    Loader().load()

    # for assistant
    Loader(path="assistant").load(log=False, exclude=["pmbot"])

    # for addons
    if addons is not False:
        url = udB.get_key("ADDONS_URL")
        if url:
            os.system("git clone -q {} addons".format(url))
        elif not os.path.exists("addons"):
            os.system(
                f"git clone -q -b {Repo().active_branch} https://github.com/TeamUltroid/UltroidAddons.git addons"
            )
        elif os.path.exists("addons/.git"):
            os.system("cd addons && git pull -q && cd ..")

        if not os.path.exists("addons"):
            os.system("git clone -q https://github.com/TeamUltroid/UltroidAddons.git addons")
        if os.path.exists("addons/addons.txt"):
            # generally addons req already there so it won't take much time
            os.system("pip3 install --no-cache-dir -q -r ./addons/addons.txt")
        Loader(path="addons", key="Addons").load(func=load_addons)

    # group manager
    if manager:
        Loader(path="assistant/manager", key="Group Manager").load(cmd_help=None)

    # chat via assistant
    if pmbot:
        Loader(path="assistant/pmbot.py").load_single(log=False)

    # vc bot
    if vcbot and not vcClient._bot:
        Loader(path="vcbot", key="VCBot").load()

# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import glob
import os
from importlib import import_module

from decouple import config
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

    def load(self, log=True, func=import_module, cmd_help=HELP, include=[], exclude=[]):
        if include:
            if log:
                self._logger.info(
                    "Including:{}".format("".join(f"• {name}" for name in include))
                )
            files = glob.glob(f"{self.path}/_*.py")
            for file in include:
                path = f"{self.path}/{file}.py"
                if os.path.exists(path):
                    files.append(path)
        else:
            files = glob.glob(f"{self.path}/*.py")
            if exclude:
                for path in exclude:
                    if not path.startswith("_"):
                        try:
                            files.remove(f"{self.path}/{path}.py")
                        except ValueError:
                            pass
        if log:
            self._logger.info(
                f"• Installing {self.key}'s Plugins || Count : {len(files)} •"
            )
        for plugin in sorted(files):
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
    _exclude = udB.get_key("EXCLUDE_OFFICIAL") or config("EXCLUDE_OFFICIAL", None)
    _exclude = _exclude.split() if _exclude else []

    # "INCLUDE_ONLY" was added to reduce Big List in "EXCLUDE_OFFICIAL" Plugin
    _in_only = udB.get_key("INCLUDE_ONLY") or config("INCLUDE_ONLY", None)
    _in_only = _in_only.split() if _in_only else []
    Loader().load(include=_in_only, exclude=_exclude)

    # for assistant
    if not udB.get_key("DISABLE_AST_PLUGINS"):
        _ast_exc = ["pmbot"]
        if _in_only and "games" not in _in_only:
            _ast_exc.append("games")
        Loader(path="assistant").load(log=False, exclude=_ast_exc)

    # for addons
    if addons:
        url = udB.get_key("ADDONS_URL")
        if url:
            os.system("git clone -q {} addons".format(url))
        if os.path.exists("addons") and not os.path.exists("addons/.git"):
            os.rmdir("addons")
        if not os.path.exists("addons"):
            os.system(
                f"git clone -q -b {Repo().active_branch} https://github.com/TeamUltroid/UltroidAddons.git addons"
            )
        else:
            os.system("cd addons && git pull -q && cd ..")

        if not os.path.exists("addons"):
            os.system(
                "git clone -q https://github.com/TeamUltroid/UltroidAddons.git addons"
            )
        if os.path.exists("addons/addons.txt"):
            # generally addons req already there so it won't take much time
            os.system(
                "rm -rf /usr/local/lib/python3.9/site-packages/pip/_vendor/.wh.appdirs.py"
            )
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
        try:
            import pytgcalls  # ignore: pylint

            Loader(path="vcbot", key="VCBot").load()
        except ModuleNotFoundError:
            LOGS.info("'pytgcalls' not installed!\nSkipping load of VcBot.")

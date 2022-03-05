# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import glob
import os
from importlib import import_module
from logging import Logger

from . import *
from .dB._core import HELP


class Loader:
    def __init__(self, path="plugins", key="Official", logger: Logger = LOGS):
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
            except ModuleNotFoundError as er:
                doc = None
                self._logger.error(f"{plugin}: '{er.name}' module not installed!")
            except Exception as exc:
                doc = None
                self._logger.error(f"Ultroid - {self.key} - ERROR - {plugin}")
                self._logger.exception(exc)
            if func == import_module:
                plugin = plugin.split(".")[-1]
            if doc and (
                (cmd_help or cmd_help == {})
                and not plugin.startswith("_")
                and (doc.__doc__)
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

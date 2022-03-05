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

from . import LOGS


class Loader:
    def __init__(self, path="plugins", key="Official", logger: Logger = LOGS):
        self.path = path
        self.key = key
        self._logger = logger

    def load(
        self, log=True, func=import_module, include=None, exclude=None, after_load=None
    ):
        if include:
            if log:
                self._logger.info("Including: {}".format("• ".join(include)))
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
                modl = func(plugin)
            except ModuleNotFoundError as er:
                modl = None
                self._logger.error(f"{plugin}: '{er.name}' module not installed!")
            except Exception as exc:
                modl = None
                self._logger.error(f"pyUltroid - {self.key} - ERROR - {plugin}")
                self._logger.exception(exc)
            if callable(after_load):
                if func == import_module:
                    plugin = plugin.split(".")[-1]
                after_load(self, modl, plugin_name=plugin)

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

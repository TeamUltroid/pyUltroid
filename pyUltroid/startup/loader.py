# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
from importlib import import_module

from git import Repo

from .. import LOGS, udB
from .utils import load_addons


class Loader:
    def __init__(self, path="plugins", key="Official"):
        self.path = path
        self.key = key

    def load(self, log=True, func=None):
        files = sorted(glob.glob(path + "/*.py"))
        for plugin in files:
            if not func:
                plugin = plugin[:-3].replace("/", ".")
                func = import_module
            try:
                func(plugin)
                if log:
                    LOGS.info(f"Ultroid - {self.key} -  Installed - {plugin}")
            except Exception as exc:
                LOGS.info(f"Ultroid - {self.key} - ERROR - {plugin}")
                LOGS.exception(exc)
        LOGS.info("-" * 70)


def load_other_plugins(addons=None, pmbot=None, manager=None, vcbot=None):

    # for assistant
    Loader(path="assistant", key="Assistant").load()

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
        Loader(path="addons", key="Addons").load(func=load_addons)

    # group manager
    if manager == "True":
        Loader(path="assistant/manager", key="Group Manager").load()

    # chat via assistant
    if pmbot == "True":
        Loader(path="assistant/pmbot", key="PM Bot").load(log=False)

    # vc bot
    if vcbot == "True":
        Loader(path="vcbot", key="VCBot").load()

# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
from shutil import rmtree

from decouple import config
from git import Repo
from .. import *
from ..dB._core import HELP
from ..loader import Loader
from . import *
from .utils import load_addons


def _after_load(loader, module, plugin_name=""):
    if module and not plugin_name.startswith("_") and (module.__doc__):
        doc = module.__doc__.format(i=HNDLR)
        if loader.key in HELP.keys():
            update_cmd = HELP[loader.key]
            try:
                update_cmd.update({plugin_name: doc})
            except BaseException as er:
                loader._logger.exception(er)
        else:
            try:
                HELP.update({loader.key: {plugin_name: doc}})
            except BaseException as em:
                loader._logger.exception(em)


def load_other_plugins(addons=None, pmbot=None, manager=None, vcbot=None):

    # for official
    _exclude = udB.get_key("EXCLUDE_OFFICIAL") or config("EXCLUDE_OFFICIAL", None)
    _exclude = _exclude.split() if _exclude else []

    # "INCLUDE_ONLY" was added to reduce Big List in "EXCLUDE_OFFICIAL" Plugin
    _in_only = udB.get_key("INCLUDE_ONLY") or config("INCLUDE_ONLY", None)
    _in_only = _in_only.split() if _in_only else []
    Loader().load(include=_in_only, exclude=_exclude, after_load=_after_load)

    # for assistant
    if not udB.get_key("DISABLE_AST_PLUGINS"):
        _ast_exc = ["pmbot"]
        if _in_only and "games" not in _in_only:
            _ast_exc.append("games")
        Loader(path="assistant").load(
            log=False, exclude=_ast_exc, after_load=_after_load
        )

    # for addons
    if addons:
        url = udB.get_key("ADDONS_URL")
        if url:
            os.system("git clone -q {} addons".format(url))
        if os.path.exists("addons") and not os.path.exists("addons/.git"):
            rmtree("addons")
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

        _exclude = udB.get_key("EXCLUDE_ADDONS")
        _exclude = _exclude.split() if _exclude else []
        _in_only = udB.get_key("INCLUDE_ADDONS")
        _in_only = _in_only.split() if _in_only else []

        Loader(path="addons", key="Addons").load(
            func=load_addons, include=_in_only, exclude=_exclude, after_load=_after_load
        )

    # group manager
    if manager:
        Loader(path="assistant/manager", key="Group Manager").load()

    # chat via assistant
    if pmbot:
        Loader(path="assistant/pmbot.py").load_single(log=False)

    # vc bot
    if vcbot and not vcClient._bot:
        try:
            import pytgcalls  # ignore: pylint
            if not os.path.isdir("vcbot/downloads"):
                os.mkdir("vcbot/downloads")
            Loader(path="vcbot", key="VCBot").load(after_load=_after_load)
        except ModuleNotFoundError:
            LOGS.error("'pytgcalls' not installed!\nSkipping load of VcBot.")

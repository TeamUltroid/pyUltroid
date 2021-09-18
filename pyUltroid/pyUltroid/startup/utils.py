# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from importlib import util
from pathlib import Path
from sys import modules


def load_plugins(plugin_name):
    if plugin_name.startswith("__"):
        pass
    else:
        from .. import HNDLR, LOGS, asst, udB, ultroid_bot
        from ..dB.core import HELP, PLUGINS
        from ..dB.database import Var
        from ..misc import _supporter as xxx
        from ..misc._assistant import (
            asst_cmd,
            callback,
            in_pattern,
            inline,
            inline_owner,
            owner,
        )
        from ..misc._decorators import ultroid_cmd
        from ..misc._wrappers import eod, eor

        path = Path(f"plugins/{plugin_name}.py")
        name = "plugins.{}".format(plugin_name)
        spec = util.spec_from_file_location(name, path)
        mod = util.module_from_spec(spec)
        mod.asst = asst
        mod.tgbot = asst
        mod.ultroid_bot = ultroid_bot
        mod.bot = ultroid_bot
        mod.ultroid = ultroid_bot
        mod.owner = owner()
        mod.in_owner = inline_owner()
        mod.inline = inline()
        mod.in_pattern = in_pattern
        mod.eod = eod
        mod.edit_delete = eod
        mod.LOGS = LOGS
        mod.hndlr = HNDLR
        mod.HNDLR = HNDLR
        mod.Var = Var
        mod.eor = eor
        mod.edit_or_reply = eor
        mod.asst_cmd = asst_cmd
        mod.ultroid_cmd = ultroid_cmd
        mod.on_cmd = ultroid_cmd
        mod.callback = callback
        mod.Redis = udB.get
        modules["support"] = xxx
        modules["userbot"] = xxx
        modules["userbot.utils"] = xxx
        modules["userbot.config"] = xxx
        spec.loader.exec_module(mod)
        modules["plugins." + plugin_name] = mod
        if not plugin_name.startswith("_"):
            if plugin_name not in PLUGINS:
                PLUGINS.append(plugin_name)
            try:
                doc = modules[f"plugins.{plugin_name}"].__doc__
                HELP.update({f"{plugin_name}": doc.format(i=HNDLR)})
            except BaseException:
                pass


# for addons


def load_addons(plugin_name):
    if plugin_name.startswith("__"):
        pass
    else:
        from .. import HNDLR, LOGS, asst, udB, ultroid_bot
        from ..dB.core import ADDONS, HELP
        from ..dB.database import Var
        from ..misc import _supporter as xxx
        from ..misc._assistant import (
            asst_cmd,
            callback,
            in_pattern,
            inline,
            inline_owner,
            owner,
        )
        from ..misc._decorators import ultroid_cmd
        from ..misc._supporter import Config, admin_cmd, sudo_cmd
        from ..misc._wrappers import eod, eor

        path = Path(f"addons/{plugin_name}.py")
        name = "addons.{}".format(plugin_name)
        spec = util.spec_from_file_location(name, path)
        mod = util.module_from_spec(spec)
        mod.asst = asst
        mod.tgbot = asst
        mod.ultroid_bot = ultroid_bot
        mod.ub = ultroid_bot
        mod.bot = ultroid_bot
        mod.ultroid = ultroid_bot
        mod.borg = ultroid_bot
        mod.telebot = ultroid_bot
        mod.jarvis = ultroid_bot
        mod.friday = ultroid_bot
        mod.owner = owner()
        mod.in_owner = inline_owner()
        mod.inline = inline()
        mod.eod = eod
        mod.edit_delete = eod
        mod.LOGS = LOGS
        mod.in_pattern = in_pattern
        mod.hndlr = HNDLR
        mod.handler = HNDLR
        mod.HNDLR = HNDLR
        mod.CMD_HNDLR = HNDLR
        mod.Config = Config
        mod.Var = Var
        mod.eor = eor
        mod.edit_or_reply = eor
        mod.asst_cmd = asst_cmd
        mod.ultroid_cmd = ultroid_cmd
        mod.on_cmd = ultroid_cmd
        mod.callback = callback
        mod.Redis = udB.get
        mod.admin_cmd = admin_cmd
        mod.sudo_cmd = sudo_cmd
        modules["ub"] = xxx
        modules["var"] = xxx
        modules["jarvis"] = xxx
        modules["support"] = xxx
        modules["userbot"] = xxx
        modules["telebot"] = xxx
        modules["fridaybot"] = xxx
        modules["jarvis.utils"] = xxx
        modules["uniborg.util"] = xxx
        modules["telebot.utils"] = xxx
        modules["userbot.utils"] = xxx
        modules["userbot.events"] = xxx
        modules["jarvis.jconfig"] = xxx
        modules["userbot.config"] = xxx
        modules["fridaybot.utils"] = xxx
        modules["fridaybot.Config"] = xxx
        modules["userbot.uniborgConfig"] = xxx
        spec.loader.exec_module(mod)
        modules["addons." + plugin_name] = mod
        if not plugin_name.startswith("_"):
            if plugin_name not in ADDONS:
                ADDONS.append(plugin_name)
            try:
                doc = modules[f"addons.{plugin_name}"].__doc__
                HELP.update({f"{plugin_name}": doc.format(i=HNDLR)})
            except BaseException:
                pass


# for assistant


def load_assistant(plugin_name):
    if plugin_name.startswith("__"):
        pass
    else:
        from .. import HNDLR, asst, udB, ultroid_bot
        from ..misc._assistant import (
            asst_cmd,
            callback,
            in_pattern,
            inline_owner,
            owner,
        )
        from ..misc._wrappers import eod, eor

        path = Path(f"assistant/{plugin_name}.py")
        name = "assistant.{}".format(plugin_name)
        spec = util.spec_from_file_location(name, path)
        mod = util.module_from_spec(spec)
        mod.ultroid_bot = ultroid_bot
        mod.ultroid = ultroid_bot
        mod.Redis = udB.get
        mod.udB = udB
        mod.bot = ultroid_bot
        mod.asst = asst
        mod.owner = owner()
        mod.in_pattern = in_pattern
        mod.in_owner = inline_owner()
        mod.eod = eod
        mod.eor = eor
        mod.callback = callback
        mod.hndlr = HNDLR
        mod.HNDLR = HNDLR
        mod.asst_cmd = asst_cmd
        spec.loader.exec_module(mod)
        modules["assistant." + plugin_name] = mod


# msg forwarder


def load_pmbot(plugin_name):
    if plugin_name.startswith("__"):
        pass
    else:
        from .. import HNDLR, asst, udB, ultroid_bot
        from ..misc._assistant import asst_cmd, callback, owner
        from ..misc._wrappers import eod, eor

        path = Path(f"assistant/pmbot/{plugin_name}.py")
        name = "assistant.pmbot.{}".format(plugin_name)
        spec = util.spec_from_file_location(name, path)
        mod = util.module_from_spec(spec)
        mod.ultroid_bot = ultroid_bot
        mod.ultroid = ultroid_bot
        mod.bot = ultroid_bot
        mod.Redis = udB.get
        mod.udB = udB
        mod.asst = asst
        mod.owner = owner()
        mod.eod = eod
        mod.eor = eor
        mod.callback = callback
        mod.hndlr = HNDLR
        mod.HNDLR = HNDLR
        mod.asst_cmd = asst_cmd
        spec.loader.exec_module(mod)
        modules["assistant.pmbot." + plugin_name] = mod


# manager


def load_manager(plugin_name):
    if plugin_name.startswith("__"):
        pass
    else:
        from .. import asst, udB, ultroid_bot
        from ..misc._assistant import asst_cmd, callback, owner
        from ..misc._decorators import ultroid_cmd
        from ..misc._wrappers import eod, eor

        path = Path(f"assistant/manager/{plugin_name}.py")
        name = "assistant.manager.{}".format(plugin_name)
        spec = util.spec_from_file_location(name, path)
        mod = util.module_from_spec(spec)
        mod.ultroid_cmd = ultroid_cmd
        mod.ultroid_bot = ultroid_bot
        mod.ultroid = ultroid_bot
        mod.eod = eod
        mod.eor = eor
        mod.callback = callback
        mod.Redis = udB.get
        mod.udB = udB
        mod.asst = asst
        mod.owner = owner()
        mod.asst_cmd = asst_cmd
        spec.loader.exec_module(mod)
        modules["assistant.manager." + plugin_name] = mod


def load_vc(plugin_name):
    if not plugin_name.startswith("__"):
        from .. import HNDLR, LOGS, asst, udB, ultroid_bot, vcClient
        from ..dB.core import VC_HELP

        path = Path(f"vcbot/{plugin_name}.py")
        name = "vcbot.{}".format(plugin_name)
        spec = util.spec_from_file_location(name, path)
        mod = util.module_from_spec(spec)
        mod.ultroid_bot = ultroid_bot
        mod.ultroid = ultroid_bot
        mod.bot = ultroid_bot
        mod.Redis = udB.get
        mod.udB = udB
        mod.asst = asst
        mod.vcClient = vcClient
        mod.LOGS = LOGS
        spec.loader.exec_module(mod)
        modules["vcbot." + plugin_name] = mod
        try:
            VC_HELP.update(
                {
                    plugin_name: modules[f"vcbot.{plugin_name}"].__doc__.format(
                        i=udB["VC_HNDLR"] if udB.get("VC_HNDLR") else HNDLR
                    )
                    + "\n"
                }
            )
        except BaseException:
            pass

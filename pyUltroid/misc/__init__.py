# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import inspect

from .. import *

CMD_HELP = {}


def sudoers():
    from .. import udB

    if udB.get("SUDOS"):
        return udB["SUDOS"].split()
    return []


def should_allow_sudo():
    from .. import udB

    return udB.get("SUDO") == "True"


def owner_and_sudos(castint=False):
    from .. import udB, ultroid_bot

    data = [str(ultroid_bot.uid), *sudoers()]
    if castint:
        return [int(a) for a in data]
    return data


# ------------------------------------------------ #


def append_or_update(load, func):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        name = inspect.stack()[1].filename.split("/")[-1].replace(".py", "")
        if load.get(name):
            return load[name].append(func)
        return load.update({name: [func]})

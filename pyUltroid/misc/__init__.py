# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .. import *

CMD_HELP = {}
OWNER_SUDOS = []
# ----------------------------------------------#


def sudoers():
    from .. import udB

    if udB.get("SUDOS"):
        return udB["SUDOS"].split()
    return []


def should_allow_sudo():
    from .. import udB

    return udB.get("SUDO") == "True"


def owner_and_sudos(castint=False):
    if OWNER_SUDOS:
        return OWNER_SUDOS
    from .. import udB, ultroid_bot

    data = [str(ultroid_bot.uid), *sudoers()]
    if castint:
        a_ = [int(a) for a in data]
        [OWNER_SUDOS.append(b) for b in a_]
        return a_
    return data


# ------------------------------------------------ #


def append_or_update(load, func, name, arggs):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        if load.get(name):
            return load[name].append((func, arggs))
        return load.update({name: [(func, arggs)]})

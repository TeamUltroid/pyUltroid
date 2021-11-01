# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .. import *

CMD_HELP = {}
# ----------------------------------------------#


def sudoers():
    if _ult_cache.get("SUDOS"):
        return _ult_cache["SUDOS"]
    from .. import udB

    if SUDOS := udB.get("SUDOS"):
        li = [int(sudo) for sudo in SUDOS.split()]
        _ult_cache["SUDOS"] = li
        return li
    return []


def should_allow_sudo():
    from .. import udB

    return udB.get("SUDO") == "True"


def owner_and_sudos():
    if _ult_cache.get("OWNER_SUDOS"):
        return _ult_cache["OWNER_SUDOS"]

    from .. import udB, ultroid_bot

    data = [int(udB.get("OWNER_ID")), *sudoers()]
    _ult_cache["OWNER_SUDOS"] = data
    return return


# ------------------------------------------------ #


def append_or_update(load, func, name, arggs):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        if load.get(name):
            return load[name].append((func, arggs))
        return load.update({name: [(func, arggs)]})

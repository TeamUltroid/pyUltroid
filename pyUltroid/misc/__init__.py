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
    from .. import _ult_cache

    if _ult_cache.get("SUDOS") is not None:
        return _ult_cache["SUDOS"]
    from .. import udB

    li = []
    if SUDOS := udB.get("SUDOS"):
        li = [int(sudo) for sudo in SUDOS.split()]
    _ult_cache["SUDOS"] = li
    return _ult_cache["SUDOS"]


def should_allow_sudo():
    from .. import udB

    return udB.get("SUDO") == "True"


def owner_and_sudos():
    from .. import _ult_cache

    if _ult_cache.get("OWNER_SUDOS") is not None:
        for sudo in sudoers():
            if sudo not in _ult_cache["OWNER_SUDOS"]:
                _ult_cache["OWNER_SUDOS"].append(sudo)
        return _ult_cache["OWNER_SUDOS"]

    from .. import udB, ultroid_bot

    data = [int(udB.get("OWNER_ID")), *sudoers()]
    _ult_cache["OWNER_SUDOS"] = data
    return _ult_cache["OWNER_SUDOS"]


# ------------------------------------------------ #


def append_or_update(load, func, name, arggs):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        if load.get(name):
            return load[name].append((func, arggs))
        return load.update({name: [(func, arggs)]})

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .. import *

CMD_HELP = {}
# ----------------------------------------------#


class _SudoManager:
    def __init__(self):
        from .. import _ult_cache, udB
        self.dB = udB
        self.sudos = _ult_cache.get("SUDOS")
        self.owner = int(udB.get("OWNER_ID"))

    def get_sudos(self):
        if self.sudos:
            return self.sudos
        list_ = []
        if SUDOS := udB.get("SUDOS"):
            li = [int(sudo) for sudo in SUDOS.split()]
        self.sudos = li
        return self.sudos

    def should_allow_sudo(self):
        return self.db.get("SUDO") == "True"

    def owner_and_sudos(self):
        return [self.owner, *self.get_sudos()]

    def add_sudo(self, id_):
        return self.sudos.append(id_)

    def remove_sudo(self, id_):
        return self.sudos.remove(_id)

_SUDO_M = _SudoManager()

# ------------------------------------------------ #


def append_or_update(load, func, name, arggs):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        if load.get(name):
            return load[name].append((func, arggs))
        return load.update({name: [(func, arggs)]})

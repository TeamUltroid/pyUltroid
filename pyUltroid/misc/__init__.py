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
        self.db = None
        self.sudos = []
        self.owner = None

    def get_sudos(self):
        if self.sudos:
            return self.sudos
        if not self.db:
            from .. import udB
            self.db = udB
        if SUDOS := self.db.get("SUDOS"):
            li = [int(sudo) for sudo in SUDOS.split()]
        self.sudos = li
        return self.sudos

    def should_allow_sudo(self):
        if not self.db:
            from .. import udB
            self.db = udB
        return self.db.get("SUDO") == "True"

    def owner_and_sudos(self):
        if not self.owner:
            from .. import udB

            self.owner = int(udB.get("OWNER_ID"))
        return [self.owner, *self.get_sudos()]

    def add_sudo(self, id_):
        return self.sudos.append(id_)

    def remove_sudo(self, id_):
        return self.sudos.remove(_id)

_SUDO_M = _SudoManager()
owner_and_sudos = _SUDO_M.owner_and_sudos
sudoers = _SUDO_M.get_sudos

# ------------------------------------------------ #


def append_or_update(load, func, name, arggs):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        if load.get(name):
            return load[name].append((func, arggs))
        return load.update({name: [(func, arggs)]})

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
        self._owner_sudos = []

    def _init_db(self):
        if not self.db:
            from .. import udB

            self.db = udB
        return self.db

    def get_sudos(self):
        if self.sudos:
            return self.sudos
        db = self._init_db()

        if SUDOS := db.get("SUDOS"):
            li = [int(sudo) for sudo in SUDOS.split()]
            self.sudos = li
        return self.sudos

    def should_allow_sudo(self):
        db = self._init_db()
        return db.get("SUDO") == "True"

    def owner_and_sudos(self):
        if self._owner_sudos:
            return self._owner_sudos

        if not self.owner:
            db = self._init_db()
            self.owner = int(db.get("OWNER_ID"))
        self._owner_sudos = [self.owner, *self.get_sudos()]
        return self._owner_sudos

    def add_sudo(self, id_):
        if self._owner_sudos:
            self._owner_sudos.append(id_)
        return self.sudos.append(id_)

    def remove_sudo(self, id_):
        if self._owner_sudos:
            self._owner_sudos.remove(id_)
        return self.sudos.remove(_id)

    def is_sudo(self, id_):
        return bool(id_ in self.get_sudos())


_SUDO_M = _SudoManager()
owner_and_sudos = _SUDO_M.owner_and_sudos
sudoers = _SUDO_M.get_sudos
is_sudo = _SUDO_M.is_sudo

# ------------------------------------------------ #


def append_or_update(load, func, name, arggs):
    if isinstance(load, list):
        return load.append(func)
    if isinstance(load, dict):
        if load.get(name):
            return load[name].append((func, arggs))
        return load.update({name: [(func, arggs)]})

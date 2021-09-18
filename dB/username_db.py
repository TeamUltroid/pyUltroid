# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB["USERNAME_DB"])
except BaseException:
    udB.set("USERNAME_DB", "{}")


def update_username(id, uname):
    ok = eval(udB["USERNAME_DB"])
    ok.update({id: uname})
    udB.set("USERNAME_DB", str(ok))


def get_username(id):
    ok = eval(udB["USERNAME_DB"])
    if ok.get(id):
        return ok[id]
    return None

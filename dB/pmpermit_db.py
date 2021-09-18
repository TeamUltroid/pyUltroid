# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB.get("PMPERMIT"))
except BaseException:
    try:
        # Transferring stuff From old format to new
        x, y = [], udB.get("PMPERMIT").split()
        for z in y:
            x.append(int(z))
        udB.set("PMPERMIT", str(x))
    except BaseException:
        udB.set("PMPERMIT", "[]")


def get_approved():
    return eval(udB.get("PMPERMIT"))


def approve_user(id):
    ok = get_approved()
    if id not in ok:
        ok.append(id)
        udB.set("PMPERMIT", str(ok))


def disapprove_user(id):
    ok = get_approved()
    if id in ok:
        ok.remove(id)
        udB.set("PMPERMIT", str(ok))


def is_approved(id):
    ok = get_approved()
    return id in ok

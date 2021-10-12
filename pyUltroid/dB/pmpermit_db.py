# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stuff():
    a = udB.get("PMPERMIT")
    if not a:
        return []
    try:
        return eval(a)
    except BaseException:
        try:
            # Transferring stuff From old format to new
            x, y = [], udB.get("PMPERMIT").split()
            for z in y:
                x.append(int(z))
            udB.set("PMPERMIT", str(x))
            return x
        except BaseException:
            pass
    return []


def get_approved():
    return get_stuff()


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

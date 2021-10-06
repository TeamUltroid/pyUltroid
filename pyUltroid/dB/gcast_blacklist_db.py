# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.
from .. import udB


def get_stuff():
    a = udB.get("GBLACKLISTS")
    if not a:
        return []
    try:
        return eval(a)
    except BaseException:
        udB.delete("GBLACKLISTS")
    return []


def get_gblacklists():
    return get_stuff()


def add_gblacklist(id):
    ok = get_gblacklists()
    if id not in ok:
        ok.append(id)
        udB.set("GBLACKLISTS", str(ok))


def rem_gblacklist(id):
    ok = get_gblacklists()
    if id in ok:
        ok.remove(id)
        udB.set("GBLACKLISTS", str(ok))


def is_gblacklisted(id):
    ok = get_gblacklists()
    return id in ok

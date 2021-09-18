# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.
from .. import udB

try:
    eval(udB["GBLACKLISTS"])
except BaseException:
    udB.set("GBLACKLISTS", "[]")


def get_gblacklists():
    return eval(udB.get("GBLACKLISTS"))


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

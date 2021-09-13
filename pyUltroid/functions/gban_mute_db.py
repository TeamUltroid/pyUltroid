# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB["GBAN"])
except BaseException:
    udB.set("GBAN", "{}")

try:
    eval(udB["GMUTE"])
except BaseException:
    udB.set("GMUTE", "{}")


def gban(user, reason):
    ok = list_gbanned()
    ok.update({user: reason if reason else "No Reasons"})
    udB.set("GBAN", str(ok))


def ungban(user):
    ok = list_gbanned()
    if ok.get(user):
        del ok[user]
        udB.set("GBAN", str(ok))


def is_gbanned(user):
    ok = list_gbanned()
    if ok.get(user):
        return ok[user]
    return False


def list_gbanned():
    ok = eval(udB.get("GBAN"))
    return ok


def gmute(user):
    ok = list_gmuted()
    ok.append(user)
    udB.set("GMUTE", str(ok))


def ungmute(user):
    ok = list_gmuted()
    if user in ok:
        ok.remove(user)
        udB.set("GMUTE", str(ok))


def is_gmuted(user):
    ok = list_gmuted()
    if user in ok:
        return True
    return False


def list_gmuted():
    ok = eval(udB.get("GMUTE"))
    return ok

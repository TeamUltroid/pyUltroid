# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    dict(eval(udB["GBAN"]))
except BaseException:
    udB.set("GBAN", "{}")

try:
    if "list" not in str(type(eval(udB["GMUTE"]))):
        udB.set("GMUTE", "[]")
except BaseException:
    udB.set("GMUTE", "[]")


def gban(user, reason):
    ok = list_gbanned()
    ok.update({user: reason or "No Reason. "})
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
    return eval(udB.get("GBAN"))


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
    return user in ok


def list_gmuted():
    return eval(udB.get("GMUTE"))

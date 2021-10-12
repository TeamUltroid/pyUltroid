# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_gban_stuff():
    a = udB.get("GBAN")
    if not a:
        return {}
    try:
        return dict(eval(a))
    except BaseException:
        udB.delete("GBAN")
    return {}


ge = udB.get("GMUTE")
if ge:
    try:
        if "list" not in str(type(eval(ge))):
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
    return get_gban_stuff()


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
    if udB.get("GMUTE"):
        return eval(udB.get("GMUTE"))
    return []

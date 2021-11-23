# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def list_gbanned():
    if x := udB.get_key("GBAN"):
        return x
    return {}


def gban(user, reason):
    ok = list_gbanned()
    ok.update({user: reason or "No Reason. "})
    return udB.set_key("GBAN", ok)


def ungban(user):
    ok = list_gbanned()
    if ok.get(user):
        del ok[user]
        return udB.set_key("GBAN", str(ok))


def is_gbanned(user):
    ok = list_gbanned()
    if ok.get(user):
        return ok[user]


def gmute(user):
    ok = list_gmuted()
    ok.append(user)
    return udB.set_key("GMUTE", ok)


def ungmute(user):
    ok = list_gmuted()
    if user in ok:
        ok.remove(user)
        return udB.set_key("GMUTE", ok)


def is_gmuted(user):
    return user in list_gmuted()


def list_gmuted():
    if x := udB.get_key("GMUTE"):
        return x
    return []

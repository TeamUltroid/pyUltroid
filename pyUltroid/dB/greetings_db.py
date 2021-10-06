# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stuff(key=None):
    kk = udB.get(key)
    if not kk:
        return {}
    try:
        return eval(kk)
    except BaseException:
        udB.delete(key)
    return {}


def add_welcome(chat, msg, media, button):
    ok = get_stuff("WELCOME")
    ok.update({chat: {"welcome": msg, "media": media, "button": button}})
    return udB.set("WELCOME", str(ok))


def get_welcome(chat):
    ok = get_stuff("WELCOME")
    wl = ok.get(chat)
    if wl:
        return wl
    return


def delete_welcome(chat):
    ok = get_stuff("WELCOME")
    wl = ok.get(chat)
    if wl:
        ok.pop(chat)
        return udB.set("WELCOME", str(ok))
    return


def add_goodbye(chat, msg, media, button):
    ok = get_stuff("GOODBYE")
    ok.update({chat: {"goodbye": msg, "media": media, "button": button}})
    return udB.set("GOODBYE", str(ok))


def get_goodbye(chat):
    ok = get_stuff("GOODBYE")
    wl = ok.get(chat)
    if wl:
        return wl
    return


def delete_goodbye(chat):
    ok = get_stuff("GOODBYE")
    wl = ok.get(chat)
    if wl:
        ok.pop(chat)
        return udB.set("GOODBYE", str(ok))
    return


def add_thanks(chat):
    x = get_stuff("THANK_MEMBERS")
    x.update({chat: True})
    return udB.set("THANK_MEMBERS", str(x))


def remove_thanks(chat):
    x = get_stuff("THANK_MEMBERS")
    if x.get(chat):
        x.pop(chat)
        return udB.set("THANK_MEMBERS", str(x))
    return


def must_thank(chat):
    x = get_stuff("THANK_MEMBERS")
    try:
        return x[chat]
    except KeyError:
        return False

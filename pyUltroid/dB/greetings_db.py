# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB.get("WELCOME"))
except BaseException:
    udB.set("WELCOME", "{}")

try:
    eval(udB.get("GOODBYE"))
except BaseException:
    udB.set("GOODBYE", "{}")

try:
    eval(udB.get("THANK_MEMBERS"))
except BaseException:
    udB.set("THANK_MEMBERS", "{}")


def add_welcome(chat, msg, media, button):
    ok = eval(udB.get("WELCOME"))
    ok.update({chat: {"welcome": msg, "media": media, "button": button}})
    return udB.set("WELCOME", str(ok))


def get_welcome(chat):
    ok = eval(udB.get("WELCOME"))
    wl = ok.get(chat)
    if wl:
        return wl
    return


def delete_welcome(chat):
    ok = eval(udB.get("WELCOME"))
    wl = ok.get(chat)
    if wl:
        ok.pop(chat)
        return udB.set("WELCOME", str(ok))
    return


def add_goodbye(chat, msg, media, button):
    ok = eval(udB.get("GOODBYE"))
    ok.update({chat: {"goodbye": msg, "media": media, "button": button}})
    return udB.set("GOODBYE", str(ok))


def get_goodbye(chat):
    ok = eval(udB.get("GOODBYE"))
    wl = ok.get(chat)
    if wl:
        return wl
    return


def delete_goodbye(chat):
    ok = eval(udB.get("GOODBYE"))
    wl = ok.get(chat)
    if wl:
        ok.pop(chat)
        return udB.set("GOODBYE", str(ok))
    return


def add_thanks(chat):
    x = eval(udB.get("THANK_MEMBERS"))
    x.update({chat: True})
    return udB.set("THANK_MEMBERS", str(x))


def remove_thanks(chat):
    x = eval(udB.get("THANK_MEMBERS"))
    if x.get(chat):
        x.pop(chat)
        return udB.set("THANK_MEMBERS", str(x))
    return


def must_thank(chat):
    x = eval(udB.get("THANK_MEMBERS"))
    try:
        return x[chat]
    except KeyError:
        return False

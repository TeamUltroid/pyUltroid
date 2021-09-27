# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB["FILTERS"])
except BaseException:
    udB.set("FILTERS", "{}")


def add_filter(chat, word, msg, media, button):
    ok = eval(udB.get("FILTERS"))
    if ok.get(chat):
        ok[chat].update({word: {"msg": msg, "media": media, "button": button}})
    else:
        ok.update({chat: {word: {"msg": msg, "media": media, "button": button}}})
    udB.set("FILTERS", str(ok))


def rem_filter(chat, word):
    ok = eval(udB.get("FILTERS"))
    if ok.get(chat) and ok[chat].get(word):
        ok[chat].pop(word)
        udB.set("FILTERS", str(ok))


def rem_all_filter(chat):
    ok = eval(udB.get("FILTERS"))
    if ok.get(chat):
        ok.pop(chat)
        udB.set("FILTERS", str(ok))


def get_filter(chat):
    ok = eval(udB.get("FILTERS"))
    if ok.get(chat):
        return ok[chat]
    return False


def list_filter(chat):
    ok = eval(udB.get("NOTE"))
    if ok.get(chat):
        return "".join(f"👉 `{z}`\n" for z in ok[chat])
    return False

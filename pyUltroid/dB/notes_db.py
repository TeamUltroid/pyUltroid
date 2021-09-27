# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB["NOTE"])
except BaseException:
    udB.set("NOTE", "{}")


def add_note(chat, word, msg, media, button):
    ok = eval(udB.get("NOTE"))
    if ok.get(chat):
        ok[chat].update({word: {"msg": msg, "media": media, "button": button}})
    else:
        ok.update({chat: {word: {"msg": msg, "media": media, "button": button}}})
    udB.set("NOTE", str(ok))


def rem_note(chat, word):
    ok = eval(udB.get("NOTE"))
    if ok.get(chat) and ok[chat].get(word):
        ok[chat].pop(word)
        udB.set("NOTE", str(ok))


def rem_all_note(chat):
    ok = eval(udB.get("NOTE"))
    if ok.get(chat):
        ok.pop(chat)
        udB.set("NOTE", str(ok))


def get_notes(chat, word):
    ok = eval(udB.get("NOTE"))
    if ok.get(chat) and ok[chat].get(word):
        return ok[chat][word]
    return False


def list_note(chat):
    ok = eval(udB.get("NOTE"))
    if ok.get(chat):
        return "".join(f"👉 #{z}\n" for z in ok[chat])
    return False

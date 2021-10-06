# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stuff():
    a = udB.get("NOTE")
    if not a:
        return {}
    try:
        return eval(a)
    except BaseException:
        udB.delete("NOTE")
    return {}


def add_note(chat, word, msg, media, button):
    ok = get_stuff()
    if ok.get(chat):
        ok[chat].update({word: {"msg": msg, "media": media, "button": button}})
    else:
        ok.update({chat: {word: {"msg": msg, "media": media, "button": button}}})
    udB.set("NOTE", str(ok))


def rem_note(chat, word):
    ok = get_stuff()
    if ok.get(chat) and ok[chat].get(word):
        ok[chat].pop(word)
        udB.set("NOTE", str(ok))


def rem_all_note(chat):
    ok = get_stuff()
    if ok.get(chat):
        ok.pop(chat)
        udB.set("NOTE", str(ok))


def get_notes(chat, word):
    ok = get_stuff()
    if ok.get(chat) and ok[chat].get(word):
        return ok[chat][word]
    return False


def list_note(chat):
    ok = get_stuff()
    if ok.get(chat):
        return "".join(f"👉 #{z}\n" for z in ok[chat])
    return False

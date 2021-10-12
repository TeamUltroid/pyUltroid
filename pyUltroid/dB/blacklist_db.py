# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stuff():
    a = udB.get("BLACKLIST_DB")
    if not a:
        return {}
    try:
        return eval(a)
    except BaseException:
        udB.delete("BLACKLIST_DB")
    return {}


def add_blacklist(chat, word):
    ok = get_stuff()
    if ok.get(chat):
        for z in word.split():
            if z not in ok[chat]:
                ok[chat].append(z)
    else:
        ok.update({chat: [word]})
    udB.set("BLACKLIST_DB", str(ok))


def rem_blacklist(chat, word):
    ok = get_stuff()
    if ok.get(chat) and word in ok[chat]:
        ok[chat].remove(word)
        udB.set("BLACKLIST_DB", str(ok))


def list_blacklist(chat):
    ok = get_stuff()
    if ok.get(chat):
        txt = "".join(f"👉`{z}`\n" for z in ok[chat])
        if txt:
            return txt
    return


def get_blacklist(chat):
    ok = get_stuff()
    if ok.get(chat):
        return ok[chat]
    return False

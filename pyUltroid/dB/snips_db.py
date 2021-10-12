# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stuff():
    a = udB.get("SNIP")
    if not a:
        return {}
    try:
        return eval(a)
    except BaseException:
        udB.delete("SNIP")
    return {}


def add_snip(word, msg, media, button):
    ok = get_stuff()
    ok.update({word: {"msg": msg, "media": media, "button": button}})
    udB.set("SNIP", str(ok))


def rem_snip(word):
    ok = get_stuff()
    if ok.get(word):
        ok.pop(word)
        udB.set("SNIP", str(ok))


def get_snips(word):
    ok = get_stuff()
    if ok.get(word):
        return ok[word]
    return False


def list_snip():
    ok = get_stuff()
    return "".join(f"👉 ${z}\n" for z in ok)

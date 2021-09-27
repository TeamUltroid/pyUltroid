# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB["SNIP"])
except BaseException:
    udB.set("SNIP", "{}")


def add_snip(word, msg, media, button):
    ok = eval(udB.get("SNIP"))
    ok.update({word: {"msg": msg, "media": media, "button": button}})
    udB.set("SNIP", str(ok))


def rem_snip(word):
    ok = eval(udB.get("SNIP"))
    if ok.get(word):
        ok.pop(word)
        udB.set("SNIP", str(ok))


def get_snips(word):
    ok = eval(udB.get("SNIP"))
    if ok.get(word):
        return ok[word]
    return False


def list_snip():
    ok = eval(udB.get("SNIP"))
    return "".join(f"👉 ${z}\n" for z in ok)

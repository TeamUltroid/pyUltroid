# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB.get("MUTE"))
except BaseException:
    udB.set("MUTE", "{}")


def mute(chat, id):
    ok = eval(udB.get("MUTE"))
    if ok.get(chat):
        if id not in ok[chat]:
            ok[chat].append(id)
    else:
        ok.update({chat: [id]})
    udB.set("MUTE", str(ok))


def unmute(chat, id):
    ok = eval(udB.get("MUTE"))
    if ok.get(chat) and id in ok[chat]:
        ok[chat].remove(id)
    udB.set("MUTE", str(ok))


def is_muted(chat, id):
    ok = eval(udB.get("MUTE"))
    return bool(ok.get(chat) and id in ok[chat])

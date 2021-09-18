# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from datetime import datetime as dt

from .. import udB

try:
    eval(udB["AFK_DB"])
except BaseException:
    udB.set("AFK_DB", "[]")


def add_afk(msg, media_type, media):
    time = dt.now().strftime("%b %d %Y %I:%M:%S%p")
    udB.set("AFK_DB", str([msg, media_type, media, time]))
    return


def is_afk():
    afk = eval(udB["AFK_DB"])
    if afk:
        start_time = dt.strptime(afk[3], "%b %d %Y %I:%M:%S%p")
        afk_since = str(dt.now().replace(microsecond=0) - start_time)
        return afk[0], afk[1], afk[2], afk_since
    return False


def del_afk():
    return udB.set("AFK_DB", "[]")

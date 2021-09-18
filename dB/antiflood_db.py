# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import ast

from .. import udB


def get_flood():
    if not udB.get("ANTIFLOOD"):
        return {}

    n = [ast.literal_eval(udB.get("ANTIFLOOD"))]
    return n[0]


def set_flood(chat_id, limit):
    omk = get_flood()
    omk[int(chat_id)] = int(limit)
    udB.set("ANTIFLOOD", str(omk))
    return True


def get_flood_limit(chat_id):
    omk = get_flood()
    if int(chat_id) in omk.keys():
        return omk[int(chat_id)]
    else:
        return None


def rem_flood(chat_id):
    omk = get_flood()
    if int(chat_id) not in omk.keys():
        return None

    try:
        del omk[int(chat_id)]
        udB.set("ANTIFLOOD", str(omk))
        return True
    except KeyError:
        return False

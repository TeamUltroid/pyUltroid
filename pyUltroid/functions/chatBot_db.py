# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB

try:
    eval(udB["CHATBOT_USERS"])
except BaseException:
    udB.set("CHATBOT_USERS", "{}")


def get_all_added(chat):
    ok = eval(udB["CHATBOT_USERS"])
    if ok.get(chat):
        return ok[chat]
    return False


def chatbot_stats(chat, id):
    ok = eval(udB["CHATBOT_USERS"])
    return bool(ok.get(chat) and id in ok[chat])


def add_chatbot(chat, id):
    ok = eval(udB["CHATBOT_USERS"])
    if not ok.get(chat):
        ok.update({chat: [id]})
    elif id not in ok[chat]:
        ok[chat].append(id)
    return udB.set("CHATBOT_USERS", str(ok))


def rem_chatbot(chat, id):
    ok = eval(udB["CHATBOT_USERS"])
    if ok.get(chat) and id in ok[chat]:
        ok[chat].remove(id)
    return udB.set("CHATBOT_USERS", str(ok))

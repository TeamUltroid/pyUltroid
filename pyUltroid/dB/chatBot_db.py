# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stuff():
    a = udB.get("CHATBOT_USERS")
    if not a:
        return {}
    try:
        return eval(a)
    except BaseException:
        udB.delete("CHATBOT_USERS")
    return {}


def get_all_added(chat):
    ok = get_stuff()
    if ok.get(chat):
        return ok[chat]
    return False


def chatbot_stats(chat, id):
    ok = get_stuff()
    return bool(ok.get(chat) and id in ok[chat])


def add_chatbot(chat, id):
    ok = get_stuff()
    if not ok.get(chat):
        ok.update({chat: [id]})
    elif id not in ok[chat]:
        ok[chat].append(id)
    return udB.set("CHATBOT_USERS", str(ok))


def rem_chatbot(chat, id):
    ok = get_stuff()
    if ok.get(chat) and id in ok[chat]:
        ok[chat].remove(id)
    return udB.set("CHATBOT_USERS", str(ok))

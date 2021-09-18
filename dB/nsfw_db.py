# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .. import udB

try:
    eval(udB.get("NSFW"))
except BaseException:
    udB.set("NSFW", "{}")
try:
    eval(udB.get("PROFANITY"))
except BaseException:
    udB.set("PROFANITY", "{}")


def nsfw_chat(chat, action):
    x = eval(udB.get("NSFW"))
    x.update({chat: action})
    return udB.set("NSFW", str(x))


def rem_nsfw(chat):
    x = eval(udB.get("NSFW"))
    if x.get(chat):
        x.pop(chat)
        return udB.set("NSFW", str(x))
    return


def is_nsfw(chat):
    x = eval(udB.get("NSFW"))
    if x.get(chat):
        return x[chat]
    return


def profan_chat(chat, action):
    x = eval(udB.get("PROFANITY"))
    x.update({chat: action})
    return udB.set("PROFANITY", str(x))


def rem_profan(chat):
    x = eval(udB.get("PROFANITY"))
    if x.get(chat):
        x.pop(chat)
        return udB.set("PROFANITY", str(x))
    return


def is_profan(chat):
    x = eval(udB.get("PROFANITY"))
    if x.get(chat):
        return x[chat]
    return

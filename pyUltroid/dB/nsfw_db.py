# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .. import udB


def get_stuff(key=None):
    kk = udB.get(key)
    if not kk:
        return {}
    try:
        return eval(kk)
    except BaseException:
        udB.delete(key)
    return {}


def nsfw_chat(chat, action):
    x = get_stuff("NSFW")
    x.update({chat: action})
    return udB.set("NSFW", str(x))


def rem_nsfw(chat):
    x = get_stuff("NSFW")
    if x.get(chat):
        x.pop(chat)
        return udB.set("NSFW", str(x))
    return


def is_nsfw(chat):
    x = get_stuff("NSFW")
    if x.get(chat):
        return x[chat]
    return


def profan_chat(chat, action):
    x = get_stuff("PROFANITY")
    x.update({chat: action})
    return udB.set("PROFANITY", str(x))


def rem_profan(chat):
    x = get_stuff("PROFANITY")
    if x.get(chat):
        x.pop(chat)
        return udB.set("PROFANITY", str(x))
    return


def is_profan(chat):
    x = get_stuff("PROFANITY")
    if x.get(chat):
        return x[chat]
    return

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stuff():
    return udB.get_key("ECHO") or {}


def add_echo(chat, user):
    x = get_stuff()
    if k := x.get(chat):
        if user not in k:
            k.append(user)
        x.update({chat: k})
    else:
        x.update({chat: [user]})
    return udB.set_key("ECHO", x)

def rem_echo(chat, user):
    x = get_stuff()
    if k := x.get(chat):
        if user in k:
            k.remove(user)
        x.update({chat: k})
    return udB.set_key("ECHO", x)


def check_echo(chat, user):
    x = get_stuff()
    if k := x.get(chat):
        if user in k:
            return True


def list_echo(chat):
    x = get_stuff()
    if k := x.get(chat):
        return k

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .. import udB


def get_stuff():
    a = udB.get("BOTCHAT")
    if a:
        try:
            return eval(a)
        except BaseException:
            udB.delete("BOTCHAT")
    return {}


def add_stuff(msg_id, user_id):
    ok = get_stuff()
    ok.update({msg_id: user_id})
    udB.set("BOTCHAT", str(ok))


def get_who(msg_id):
    ok = get_stuff()
    if ok.get(msg_id):
        return ok[msg_id]
    return


def tag_add(msg, chat, user):
    ok = get_stuff()
    if not ok.get("TAG"):
        ok.update({"TAG": {msg: [chat, user]}})
    else:
        ok["TAG"].update({msg: [chat, user]})
    udB.set("BOTCHAT", str(ok))


def who_tag(msg):
    ok = get_stuff()
    if ok.get("TAG") and ok["TAG"].get(msg):
        return ok["TAG"][msg]
    return False, False

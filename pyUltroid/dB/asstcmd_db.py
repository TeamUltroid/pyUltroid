# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .. import udB


def get_stuff():
    a = udB.get("ASST_CMDS")
    if not a:
        return {}
    try:
        return eval(a)
    except BaseException:
        udB.delete("ASST_CMDS")
    return {}


def add_cmd(cmd, msg, media, button):
    ok = get_stuff()
    ok.update({cmd: {"msg": msg, "media": media, "button": button}})
    return udB.set("ASST_CMDS", str(ok))


def rem_cmd(cmd):
    ok = get_stuff()
    if ok.get(cmd):
        ok.pop(cmd)
        return udB.set("ASST_CMDS", str(ok))
    return


def cmd_reply(cmd):
    ok = get_stuff()
    if ok.get(cmd):
        okk = ok[cmd]
        return okk["msg"], okk["media"], okk["button"] if ok.get("button") else None
    return


def list_cmds():
    ok = get_stuff()
    if ok.keys():
        return ok.keys()
    return {}

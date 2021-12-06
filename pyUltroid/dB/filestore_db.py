# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def get_stored():
    stored = udB.get("FILE_STORE")
    if stored is None:
        return {}
    try:
        return eval(stored)
    except BaseException:
        udB.delete("FILE_STORE")
    return {}


def store_msg(hash, msg_id):
    all = get_stored()
    all.update({hash: msg_id})
    udB.set_key("FILE_STORE", str(all))


def list_all_stored_msgs():
    all = get_stored()
    return [i for i in all]


def get_stored_msg(hash):
    all = get_stored()
    if all[hash]:
        return all[hash]
    return None

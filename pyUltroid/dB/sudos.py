# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import _ult_cache, udB, ultroid_bot
from ..misc import sudoers


def str_to_list(text):  # Returns List
    return text.split(" ")


def list_to_str(list_):  # Returns String
    str_ = "".join(f"{x} " for x in list_)
    return str_.strip()


def are_all_nums(list_):  # Takes List , Returns Boolean
    return all(item.isdigit() for item in list_)


get_sudos = sudoers


def is_sudo(id_):  # Take int or str with numbers only , Returns Boolean
    if not str(id_).isdigit():
        return False
    sudos = get_sudos()
    return str(id_) in sudos


def add_sudo(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        sudos = get_sudos()
        sudos.append(id_)
        _ult_cache["SUDOS"].append(id_)
        if _ult_cache.get("OWNER_SUDOS"):
            _ult_cache["OWNER_SUDOS"].append(id_)
        udB.set("SUDOS", list_to_str(sudos))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/sudos/add_sudo : {e}")
        return False


def del_sudo(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        sudos = get_sudos()
        sudos.remove(id_)
        _ult_cache["SUDOS"].remove(id_)
        if _ult_cache.get("OWNER_SUDOS"):
            _ult_cache["OWNER_SUDOS"].remove(id_)
        udB.set("SUDOS", list_to_str(sudos))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/sudos/del_sudo : {e}")
        return False


def is_fullsudo(id_):
    if id_ == ultroid_bot.uid:
        return True
    id_ = str(id_)
    x = udB.get("FULLSUDO")
    if x and id_ in x:
        return True
    return

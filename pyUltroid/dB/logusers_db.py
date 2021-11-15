# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def str_to_list(text):  # Returns List
    return text.split(" ")


def list_to_str(list_):  # Returns String
    str_ = "".join(f"{x} " for x in list_)
    return str_.strip()


def get_logger():  # Returns List
    pmperm = udB.get_key("LOGUSERS")
    if not pmperm:
        return [""]
    return str_to_list(pmperm)


def is_logger(id_):  # Take int or str with numbers only , Returns Boolean
    if not str(id_).isdigit():
        return False
    pmperm = get_logger()
    return str(id_) in pmperm


def log_user(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        pmperm = get_logger()
        pmperm.append(id_)
        udB.set("LOGUSERS", list_to_str(pmperm))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/logusers_db/log_user : {e}")
        return False


def nolog_user(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        pmperm = get_logger()
        pmperm.remove(id_)
        udB.set("LOGUSERS", list_to_str(pmperm))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/loguser_db/nolog_user : {e}")
        return False

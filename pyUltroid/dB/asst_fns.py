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


def is_added(id_):  # Take int or str with numbers only , Returns Boolean
    if not str(id_).isdigit():
        return False
    users = get_all_users()
    return str(id_) in users


def add_user(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        users = get_all_users()
        users.append(id_)
        udB.set("BOT_USERS", list_to_str(users))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/pmbot/add_user : {e}")
        return False


def del_user(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        users = get_all_users()
        users.remove(id_)
        udB.set("BOT_USERS", list_to_str(users))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/pmbot/del_user : {e}")
        return False


def get_all_users():  # Returns List
    users = udB.get("BOT_USERS")
    if not users:
        return [""]
    return str_to_list(users)


def is_blacklisted(id_):  # Take int or str with numbers only , Returns Boolean
    if not str(id_).isdigit():
        return False
    users = get_all_bl_users()
    return str(id_) in users


def blacklist_user(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        users = get_all_bl_users()
        users.append(id_)
        udB.set("BOT_BLS", list_to_str(users))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/pmbot/blacklist_user : {e}")
        return False


def rem_blacklist(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    if not id_.isdigit():
        return False
    try:
        users = get_all_bl_users()
        users.remove(id_)
        udB.set("BOT_BLS", list_to_str(users))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/pmbot/rem_blacklist : {e}")
        return False


def get_all_bl_users():  # Returns List
    users = udB.get("BOT_BLS")
    if not users:
        return [""]
    return str_to_list(users)

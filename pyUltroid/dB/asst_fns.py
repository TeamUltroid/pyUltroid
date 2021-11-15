# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def is_added(id_):  # Take int or str with numbers only , Returns Boolean
    return id_ in get_all_users()


def add_user(id_):  # Take int or str with numbers only , Returns Boolean
    try:
        users = get_all_users()
        users.append(id_)
        udB.set_key("BOT_USERS", users)
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/pmbot/add_user : {e}")
        return False


def get_all_users():  # Returns List
    users = udB.get_key("BOT_USERS")
    if not users:
        return []
    if isinstance(users, str):
        return [int(user) for user in users.split()]
    return users


def is_blacklisted(id_):  # Take int or str with numbers only , Returns Boolean
    return id_ in get_all_bl_users()


def blacklist_user(id_):  # Take int or str with numbers only , Returns Boolean
    try:
        users = get_all_bl_users()
        users.append(id_)
        udB.set_key("BOT_BLS", users)
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/pmbot/blacklist_user : {e}")
        return False


def rem_blacklist(id_):  # Take int or str with numbers only , Returns Boolean
    try:
        users = get_all_bl_users()
        users.remove(id_)
        udB.set_key("BOT_BLS", users)
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/pmbot/rem_blacklist : {e}")
        return False


def get_all_bl_users():  # Returns List
    users = udB.get_key("BOT_BLS")
    if not users:
        return []
    if isinstance(users, str):
        return [int(user) for user in users.split()]
    return users

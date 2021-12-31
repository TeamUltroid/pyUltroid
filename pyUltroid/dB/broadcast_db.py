# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
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


def are_all_nums(list_):  # Takes List , Returns Boolean
    return all(item.isdigit() for item in list_)


def get_channels():  # Returns List
    channels = udB.get_key("BROADCAST")
    if not channels:
        return [""]
    return str_to_list(channels)


def get_no_channels():  # Returns List
    channels = udB.get_key("BROADCAST")
    if not channels:
        return 0
    return len(channels.split(" "))


def is_channel_added(id_):
    channels = get_channels()
    return str(id_) in channels


def add_channel(id_):  # Take int or str with numbers only , Returns Boolean
    id_ = str(id_)
    try:
        channels = get_channels()
        channels.append(id_)
        udB.set_key("BROADCAST", list_to_str(channels))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/broadcast_db/add_channel : {e}")
        return False


def rem_channel(id_):
    try:
        channels = get_channels()
        channels.remove(str(id_))
        udB.set_key("BROADCAST", list_to_str(channels))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/broadcast_db/rem_channel : {e}")
        return False

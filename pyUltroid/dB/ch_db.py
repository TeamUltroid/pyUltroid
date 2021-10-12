# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import udB


def str_to_list(text):  # Returns List
    return text.split(" ")


def list_to_str(list):  # Returns String
    str = "".join(f"{x} " for x in list)
    return str.strip()


def are_all_num(list):  # Takes List , Returns Boolean
    return all(item.isdigit() for item in list)


def get_source_channels():  # Returns List
    channels = udB.get("CH_SOURCE")
    if channels is None or channels == "":
        return [""]
    else:
        return str_to_list(channels)


def get_no_source_channels():  # Returns List
    channels = udB.get("CH_SOURCE")
    if channels is None or channels == "":
        return 0
    else:
        a = channels.split(" ")
    return len(a)


def is_source_channel_added(id):
    channels = get_source_channels()
    return str(id) in channels


def add_source_channel(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    try:
        channels = get_source_channels()
        channels.append(id)
        udB.set("CH_SOURCE", list_to_str(channels))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/broadcast_db/add_channel : {e}")
        return False


def rem_source_channel(id):
    try:
        channels = get_source_channels()
        channels.remove(str(id))
        udB.set("CH_SOURCE", list_to_str(channels))
        return True
    except Exception:
        return False


#########################


def get_destinations():  # Returns List
    channels = udB.get("CH_DESTINATION")
    if channels is None or channels == "":
        return [""]
    else:
        return str_to_list(channels)


def get_no_destinations():  # Returns List
    channels = udB.get("CH_DESTINATION")
    if channels is None or channels == "":
        return 0
    else:
        a = channels.split(" ")
    return len(a)


def is_destination_added(id):
    channels = get_destinations()
    return str(id) in channels


def add_destination(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    try:
        channels = get_destinations()
        channels.append(id)
        udB.set("CH_DESTINATION", list_to_str(channels))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/broadcast_db/add_channel : {e}")
        return False


def rem_destination(id):
    try:
        channels = get_destinations()
        channels.remove(str(id))
        udB.set("CH_DESTINATION", list_to_str(channels))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/broadcast_db/rem_channel : {e}")
        return False

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


def are_all_nums(list):  # Takes List , Returns Boolean
    return all(item.isdigit() for item in list)


def get_vcsudos():  # Returns List
    sudos = udB.get("VC_SUDOS")
    if sudos is None or sudos == "":
        return [""]
    else:
        return str_to_list(sudos)


def is_vcsudo(id):  # Take int or str with numbers only , Returns Boolean
    if not str(id).isdigit():
        return False
    sudos = get_vcsudos()
    return str(id) in sudos


def add_vcsudo(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    if not id.isdigit():
        return False
    try:
        sudos = get_vcsudos()
        sudos.append(id)
        udB.set("VC_SUDOS", list_to_str(sudos))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/sudos/add_sudo : {e}")
        return False


def del_vcsudo(id):  # Take int or str with numbers only , Returns Boolean
    id = str(id)
    if not id.isdigit():
        return False
    try:
        sudos = get_vcsudos()
        sudos.remove(id)
        udB.set("VC_SUDOS", list_to_str(sudos))
        return True
    except Exception as e:
        print(f"Ultroid LOG : // functions/sudos/del_sudo : {e}")
        return False

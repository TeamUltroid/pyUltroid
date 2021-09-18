# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

#from .. import LOGS, asst, udB, ultroid_bot  # pylint ignore

CMD_HELP = {}


def sudoers():
    if udB.get("SUDOS"):
        return udB["SUDOS"].split()
    return []


def should_allow_sudo():
    return udB.get("SUDO") == "True"


def owner_and_sudos():
    return [str(ultroid_bot.uid), *sudoers()]

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import *

CMD_HELP = {}


def sudoers():
#    from .. import udB

    if udB.get("SUDOS"):
        return udB["SUDOS"].split()
    return []


def should_allow_sudo():
#    from .. import udB

    return udB.get("SUDO") == "True"


def owner_and_sudos():
#    from .. import udB, ultroid_bot

    return [str(ultroid_bot.uid), *sudoers()]

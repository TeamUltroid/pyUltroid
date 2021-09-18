# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from safety.tools import *

from .startup.connections import *

LOGS = LOGS

udB = redis_connection()

ultroid_bot, asst = client_connection()

vcClient = vc_connection(udB, ultroid_bot)

if not udB.get("HNDLR"):
    udB.set("HNDLR", ".")

if not udB.get("SUDO"):
    udB.set("SUDO", "False")

if not udB.get("SUDOS"):
    udB.set("SUDOS", "777000")

if not udB.get("BLACKLIST_CHATS"):
    udB.set("BLACKLIST_CHATS", "[]")

HNDLR = udB.get("HNDLR")

if not udB.get("DUAL_HNDLR"):
    udB.set("DUAL_HNDLR", "/")

Evar = udB.get("SUDO_HNDLR")
SUDO_HNDLR = Evar if Evar else HNDLR

Hosted_On = where_hosted()

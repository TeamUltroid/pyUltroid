# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import sys
import struct
import base64
from telethon.sessions.string import CURRENT_VERSION, _STRUCT_PREFORMAT, StringSession
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError

from ..configs import Var
from . import *
from .BaseClient import UltroidClient

_PYRO_FORM = {
351:">B?256sI?",
356:">B?256sQ?",
362:">BI?256sQ?"}

def validate_session(session, logger):
    if session:
        # Telethon Session
        if session.startswith(CURRENT_VERSION):
            if len(session.strip()) != 353:
                logger.exception("Wrong string session. Copy paste correctly!")
                sys.exit()
            return StringSession(session)
        # Pyrogram Session
        elif len(session) in _PYRO_FORM.keys():
            dc_id, _, auth_key, __, ___ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" * (-len(session) % 4))
            )
            return StringSession(CURRENT_VERSION + StringSession.encode(struct.pack(
            _STRUCT_PREFORMAT.format(len(ip)),
            dc_id,
            b'\x95\x9a\xa73',
            443,
            auth_key
            )))
    logger.exception("No String Session found. Quitting...")
    sys.exit()


def vc_connection(udB, ultroid_bot):
    VC_SESSION = Var.VC_SESSION or udB.get_key("VC_SESSION")
    if VC_SESSION and VC_SESSION != Var.SESSION:
        try:
            return UltroidClient(
                StringSession(VC_SESSION), log_attempt=False, handle_auth_error=False
            )
        except (AuthKeyDuplicatedError, EOFError):
            LOGS.info(
                "Your VC_SESSION Expired. Deleting VC_SESSION from redis..."
                + "\nRenew/Change it to Use Voice/Video Chat from VC Account..."
            )
            udB.del_key("VC_SESSION")
        except Exception as er:
            LOGS.info("While creating Client for VC.")
            LOGS.exception(er)
    return ultroid_bot

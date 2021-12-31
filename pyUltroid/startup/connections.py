# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os

from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.sessions import StringSession

from ..configs import Var
from . import *
from .BaseClient import UltroidClient


def session_file(logger):
    if Var.SESSION:
        if len(Var.SESSION.strip()) != 353:
            logger.exception("Wrong string session. Copy paste correctly!")
            import sys

            sys.exit()
        return StringSession(Var.SESSION)
    else:
        logger.exception("No String Session found. Quitting...")
        import sys

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


def where_hosted():
    if os.getenv("DYNO"):
        return "heroku"
    if os.getenv("RAILWAY_GIT_REPO_NAME"):
        return "railway"
    if os.getenv("KUBERNETES_PORT"):
        return "qovery"
    if os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
        return "windows"
    if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
        return "github actions"
    if os.getenv("ANDROID_ROOT"):
        return "termux"
    return "local"

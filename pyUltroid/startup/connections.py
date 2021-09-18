# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import time

from redis import Redis
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.sessions import StringSession

from .. import LOGS
from ..configs import Var


class RedisConnection(Redis):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        password: str = None,
        platform: str = None,
    ):
        if port:
            port = port
        elif ":" in host and not port:
            port = int(host.split(":")[1])
        else:
            return "Port Number not found"

        if platform.lower() in [
            "heroku",
            "github actions",
            "local",
            "termux",
            "windows",
        ]:
            return self.connect_redis(host=host, port=port, password=password)

        elif platform.lower() == "qovery":
            if not host:
                vars, hash, host, port, password = "", "", "", 0, ""
                for vars in os.environ:
                    if vars.startswith("QOVERY_REDIS_") and vars.endswith("_HOST"):
                        var = vars
                if var != "":
                    hash = var.split("_", maxsplit=2)[1].split("_")[0]
                if hash != "":
                    host = os.environ(f"QOVERY_REDIS_{hash}_HOST")
                    port = os.environ(f"QOVERY_REDIS_{hash}_PORT")
                    password = os.environ(f"QOVERY_REDIS_{hash}_PASSWORD")
                    return self.connect_redis(host=host, port=port, password=password)
            return self.connect_redis(host=host, port=port, password=password)

    def connect_redis(self, **kwargs):
        database = Redis(**kwargs, decode_responses=True)
        try:
            database.ping()
            LOGS.info("Connected to Redis Database")
        except BaseException:
            LOGS.warning("Reconnecting to Redis Database!")
            time.sleep(5)
            self.connect_redis(**kwargs)


def session_file():
    if Var.SESSION:
        _session = StringSession(Var.SESSION)
    elif os.path.exists("client-session.session"):
        _session = "client-session"
    else:
        LOGS.info("No String Session found. Quitting...")
        exit(1)
    return _session


def vc_connection(udB, ultroid_bot):
    VC_SESSION = Var.VC_SESSION or udB.get("VC_SESSION")
    if VC_SESSION:
        if VC_SESSION == Var.SESSION:
            return ultroid_bot
        try:
            return TelegramClient(
                StringSession(VC_SESSION), api_id=Var.API_ID, api_hash=Var.API_HASH
            ).start()
        except (AuthKeyDuplicatedError, EOFError):
            LOGS.info("Your VC_SESSION Expired. Deleting VC_SESSION from redis...")
            LOGS.info("Renew/Change it to Use Voice/Video Chat from VC Account...")
            udB.delete("VC_SESSION")
        except Exception as er:
            LOGS.error("VC_SESSION: {}".format(str(er)))
    return ultroid_bot


def where_hosted():
    if os.getenv("DYNO"):
        return "heroku"
    elif os.getenv("RAILWAY_GIT_REPO_NAME"):
        return "railway"
    elif os.getenv("KUBERNETES_PORT"):
        return "qovery"
    elif os.getenv("HOSTNAME"):
        return "github actions"
    elif os.getenv("ANDROID_ROOT"):
        return "termux"
    elif os.getenv("WINDOW"):
        return "windows"
    return "local"

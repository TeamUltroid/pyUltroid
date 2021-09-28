# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os

from redis import Redis

# from safety.tools import *  # disable: pylint
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.sessions import StringSession

from ..configs import Var
from . import *
from .exceptions import RedisError

# from pyUltroid import LOGS


class RedisConnection(Redis):
    def __init__(
        self,
        host,
        password,
        platform=None,
        logger=LOGS,
        *args,
        **kwargs,
    ):
        if ":" in host:
            spli_ = host.split(":")
            host = spli_[0]
            port = int(spli_[-1])
            if host.startswith("http"):
                raise RedisError("Your REDIS_URI should not start with http !")
        else:
            raise RedisError("Port Number not found")

        kwargs["host"] = host
        kwargs["password"] = password
        kwargs["port"] = port

        if platform.lower() == "qovery" and not host:
            var, hash, host, password = "", "", "", ""
            for vars in os.environ:
                if vars.startswith("QOVERY_REDIS_") and vars.endswith("_HOST"):
                    var = vars
            if var:
                hash = var.split("_", maxsplit=2)[1].split("_")[0]
            if hash:
                kwargs["host"] = os.environ(f"QOVERY_REDIS_{hash}_HOST")
                kwargs["port"] = os.environ(f"QOVERY_REDIS_{hash}_PORT")
                kwargs["password"] = os.environ(f"QOVERY_REDIS_{hash}_PASSWORD")
        if logger:
            logger.info("Connecting to redis database")
        super().__init__(**kwargs)

    def set_redis(self, key, value):
        return self.set(str(key), str(value))

    def get_redis(self, key):
        data = None
        if self.get(str(key)):
            try:
                data = eval(self.get(str(key)))
            except BaseException:
                data = self.get(str(key))
        return data

    def del_redis(self, key):
        return bool(self.delete(str(key)))


def session_file():
    if Var.SESSION:
        _session = StringSession(Var.SESSION)
    elif os.path.exists("client-session.session"):
        _session = "client-session"
    else:
        raise Exception("No String Session found. Quitting...")
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
    elif os.getenv("WINDOW") and os.getenv("WINDOW") != "0":
        return "windows"
    elif os.getenv("HOSTNAME"):
        return "github actions"
    elif os.getenv("ANDROID_ROOT"):
        return "termux"
    return "local"

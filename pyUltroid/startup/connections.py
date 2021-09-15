# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import time
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger

from redis import Redis
from telethon import TelegramClient
from telethon import __version__ as vers
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError, PhoneNumberInvalidError
from telethon.sessions import StringSession

from ..dB._database import Var
from ..version import __version__ as ver
from ..version import ultroid_version
from .exceptions import RedisError

LOGS = getLogger("pyUltLog")

if os.path.exists("ultroid.log"):
    os.remove("ultroid.log")

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] - %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler("ultroid.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)
LOGS.info(f"py-Ultroid Version - {ver}")
LOGS.info(f"Telethon Version - {vers}")
LOGS.info(f"Ultroid Version - {ultroid_version}")


class RedisConnection(Redis):
    def __init__(
        self,
        host: str = None,
        port: int = None,
        password: str = None,
        platform: str,
    ):
        if port:
            port = self.port
        elif ":" in host and not port:
            port = int(self.host.split(":")[1])
        else:
            raise RedisError("Port Number not found")

        if platform.lower() in ["heroku", "github actions", "local", "termux"]:
            return self.connect_redis(host=self.host, port=port, password=self.password)

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
            return self.connect_redis(host=self.host, port=port, password=self.password)

    def connect_redis(self, **kwargs):
        database = Redis(**kwargs, decode_responses=True)
        try:
            database.ping()
            LOGS.info("Connected to Redis Database")
        except BaseException:
            LOGS.warning("Reconnecting to Redis Database!")
            time.sleep(5)
            self.connect_redis(**kwargs)


def def_redis_connection():
    redis_info = Var.REDIS_URI
    redis_pass = Var.REDIS_PASSWORD
    err = ""
    if ":" not in redis_info:
        err += "\nWrong REDIS_URI. Quitting...\n"
    if "/" in redis_info:
        err += "Your REDIS_URI should start with redis.xyz. Quitting...\n"
    redis_info = redis_info.replace("\n", "").replace(" ", "")
    redis_pass = redis_pass.replace("\n", "").replace(" ", "")
    if err:
        LOGS.info(err)
        exit(1)
    redis_info = redis_info.split(":")
    LOGS.info("Getting Connection With Redis Database")
    time.sleep(3.5)
    return redis.Redis(
        host=redis_info[0],
        port=redis_info[1],
        password=redis_pass,
        decode_responses=True,
    )


def redis_connection():
    our_db = connect_redis()
    time.sleep(5)
    try:
        our_db.ping()
    except BaseException:
        connected = []
        LOGS.info("Can't connect to Redis Database.... Restarting....")
        for x in range(1, 6):
            try:
                our_db = connect_redis()
                time.sleep(3)
                if our_db.ping():
                    connected.append(1)
                    break
            except BaseException as conn:
                LOGS.info(
                    f"{(conn)}\nConnection Failed ...  Trying To Reconnect {x}/5 .."
                )
        if not connected:
            LOGS.info("Redis Connection Failed.....")
            exit(1)
        else:
            LOGS.info("Reconnected To Redis Server Succesfully")
    LOGS.info("Succesfully Established Connection With Redis DataBase.")
    return our_db


def session_file():
    if os.path.exists("client-session.session"):
        _session = "client-session"
    elif Var.SESSION:
        _session = StringSession(Var.SESSION)
    else:
        LOGS.info("No String Session found. Quitting...")
        exit(1)
    return _session


def client_connection(String=None, only_user=False):
    if not String:
        String = session_file()
    client = TelegramClient(String, Var.API_ID, Var.API_HASH)
    if only_user:
        return client
    bot_client = TelegramClient(None, api_id=Var.API_ID, api_hash=Var.API_HASH)
    return client, bot_client


def vc_connection(udB, ultroid_bot):
    VC_SESSION = Var.VC_SESSION or udB.get("VC_SESSION")
    if VC_SESSION:
        if VC_SESSION == Var.SESSION:
            return ultroid_bot
        try:
            return TelegramClient(
                StringSession(VC_SESSION), api_id=Var.API_ID, api_hash=Var.API_HASH
            ).start()
        except (AuthKeyDuplicatedError, PhoneNumberInvalidError, EOFError):
            LOGS.info("Your VC_SESSION Expired. Deleting VC_SESSION from redis...")
            LOGS.info("Renew/Change it to Use Voice/Video Chat from VC Account...")
            udB.delete("VC_SESSION")
        except Exception as er:
            LOGS.info("VC_SESSION: {}".format(str(er)))
    return ultroid_bot


def connect_qovery_redis():
    uri = Var.REDIS_URI
    passw = Var.REDIS_PASSWORD
    if not uri and not passw:
        var = ""
        for i in os.environ:
            if i.startswith("QOVERY_REDIS_") and i.endswith("_PORT"):
                var = i
        if var:
            try:
                hash = var.split("QOVERY_REDIS_")[1].split("_")[0]
                # or config(f"QOVERY_REDIS_{hash}_HOST")
                endpoint = os.environ[f"QOVERY_REDIS_{hash}_HOST"]
                # or config(f"QOVERY_REDIS_{hash}_PORT")
                port = os.environ[f"QOVERY_REDIS_{hash}_PORT"]
                # or config(f"QOVERY_REDIS_{hash}_PASSWORD")
                passw = os.environ[f"QOVERY_REDIS_{hash}_PASSWORD"]
            except KeyError:
                LOGS.info("Redis Vars are missing. Quitting.")
                exit(1)
            except Exception as er:
                LOGS.info(er)
                exit(1)
            # uri = endpoint + ":" + str(port)
    return redis.Redis(
        host=endpoint,
        port=str(port),
        password=passw,
        decode_responses=True,
    )
    # return uri, passw


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
        return "win"
    return "local"

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from os import environ

class Var:
    # mandatory
    API_ID = environ.get("API_ID", default=6, cast=int)
    API_HASH = environ.get("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    BOT_TOKEN = environ.get("BOT_TOKEN", default=None)
    SESSION = environ.get("SESSION", default=None)
    REDIS_URI = environ.get("REDIS_URI", default=None)
    REDIS_PASSWORD = environ.get("REDIS_PASSWORD", default=None)
    # extras
    LOG_CHANNEL = envrion.get("LOG_CHANNEL", default=0, cast=int)
    HEROKU_APP_NAME = environ.get("HEROKU_APP_NAME", default=None)
    HEROKU_API = envrion.get("HEROKU_API", default=None)
    VC_SESSION = envrion.get("VC_SESSION", default=None)
    ADDONS = envrion.get("ADDONS", default="True")
    VCBOT = envrion.get("VCBOT", default="True")
    # for railway
    REDISPASSWORD = envrion.get("REDISPASSWORD", default=None)
    REDISHOST = envrion.get("REDISHOST", default=None)
    REDISPORT = envrion.get("REDISPORT", default=None)
    REDISUSER = envrion.get("REDISUSER", default=None)
    # for deta base
    DETA_KEY = envrion.get("DETA_KEY", default=None)
    # for future
    MULTI_SESSIONS = envrion.get("MULTI_SESSIONS", default=None)

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from re import findall

from telethon import TelegramClient
from telethon.errors import (
    AccessTokenExpiredError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)
from telethon.network.connection import (
    ConnectionTcpMTProxyRandomizedIntermediate as MtProxy,
)
from telethon.utils import get_display_name

from ..configs import Var
from . import *


class UltroidClient(TelegramClient):
    def __init__(
        self,
        session,
        proxy=None,
        bot_token=None,
        udB=None,
        logger=LOGS,
        *args,
        **kwargs,
    ):
        self.logger = logger
        self.udB = udB
        kwargs["api_id"] = Var.API_ID
        kwargs["api_hash"] = Var.API_HASH
        kwargs["base_logger"] = TelethonLogger
        kwargs["connection"] = MtProxy
        super().__init__(session, **kwargs)
        self.run_in_loop(self.start_client(bot_token=bot_token))
        self.run_in_loop(self.connect_proxy(proxy))

    async def start_client(self, **kwargs):
        """function to start client"""
        self.logger.info("Trying to login.")
        try:
            await self.start(**kwargs)
        except (AuthKeyDuplicatedError, ApiIdInvalidError, EOFError):
            self.logger.error("String session expired. Create new!")
            exit()
        except AccessTokenExpiredError:
            # AccessTokenError can only occur for Bot account
            # And at Early Process, Its saved in Redis.
            self.udB.delete("BOT_TOKEN")
            self.logger.error(
                "Bot token expired. Create new from @Botfather and add in BOT_TOKEN env variable!"
            )
            exit()
        except BaseException as er:
            self.logger.exception(er)
            exit()
        # Save some stuff for later use...
        self.me = await self.get_me()
        if self.me.bot:
            self.logger.info(f"Logged in as @{self.me.username}")
        else:
            setattr(self.me, "phone", None)
            self.logger.info(f"Logged in as {self.full_name}")

    def run_in_loop(self, function):
        """run inside asyncio loop"""
        return self.loop.run_until_complete(function)

    def run(self):
        """run asyncio loop"""
        self.run_until_disconnected()

    async def connect_proxy(self, proxy):
        if not proxy:
            return
        _proxy = findall("\\=([^&]+)", proxy)
        if findall("socks", proxy):
            proxy = ("socks5", _proxy[0], int(_proxy[1]))
        else:
            proxy = (_proxy[0], int(_proxy[1]), _proxy[2])
        self.set_proxy(proxy)
        try:
            await self.start()
        except ValueError as er:
            return self.logger.info(f"{er}\nUnSupported Proxy Used..")
        except Exception as er:
            return self.logger.exception(er)
        self.logger.info("Connected to Proxy!")

    @property
    def full_name(self):
        """full name of Client"""
        return get_display_name(self.me)

    @property
    def uid(self):
        """Client's user id"""
        return self.me.id

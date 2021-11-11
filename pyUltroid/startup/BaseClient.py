# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


import time
from re import findall

from telethon import TelegramClient
from telethon import utils as telethon_utils
from telethon.errors import (
    AccessTokenExpiredError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)
from telethon.network.connection import (
    ConnectionTcpMTProxyRandomizedIntermediate as MtProxy,
)

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
        self._ul_dl_cache = {}
        self._cache = {}
        self.logger = logger
        self.udB = udB
        self.proxy = proxy
        kwargs["api_id"] = Var.API_ID
        kwargs["api_hash"] = Var.API_HASH
        kwargs["base_logger"] = TelethonLogger
        if proxy:
            try:
                _proxy = findall("\\=([^&]+)", proxy)
                if findall("socks", proxy):
                    kwargs["proxy"] = ("socks5", _proxy[0], int(_proxy[1]))
                else:
                    kwargs["connection"] = MtProxy
                    kwargs["proxy"] = (_proxy[0], int(_proxy[1]), _proxy[2])
            except ValueError:
                kwargs["connection"] = None
                kwargs["proxy"] = None
        super().__init__(session, **kwargs)
        try:
            self.run_in_loop(self.start_client(bot_token=bot_token))
        except ValueError as er:
            LOGS.info(er)
            if proxy:
                udB.delete("TG_PROXY")
                del kwargs["connection"]
                del kwargs["proxy"]
            super().__init__(session, **kwargs)
            self.run_in_loop(self.start_client(bot_token=bot_token))
        self.dc_id = self.session.dc_id

    async def start_client(self, **kwargs):
        """function to start client"""
        self.logger.info("Trying to login.")
        try:
            await self.start(**kwargs)
        except ApiIdInvalidError:
            self.logger.error("API ID and API_HASH combination does not match!")
            exit()
        except (AuthKeyDuplicatedError, EOFError):
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
        # Save some stuff for later use...
        myself = self.udB.get("OWNER_ID")
        self.me = await self.get_me()
        if self.me.bot:
            if myself and self.me.id == int(myself):
                self.me = await self.get_entity(int(myself))
            self.logger.info(f"Logged in as @{self.me.username}")
        else:
            setattr(self.me, "phone", None)
            self.logger.info(f"Logged in as {self.full_name}")

    async def fast_uploader(self, file, **kwargs):
        """Upload files in a faster way"""

        import os
        from pathlib import Path

        start_time = time.time()
        filename = kwargs.get("filename", None)
        event = kwargs.get("event", None)
        use_cache = kwargs.get("use_cache", True)
        path = Path(file)
        size = os.path.getsize(file)
        if not filename:
            filename = path.name
        message = kwargs.get("message", f"Uploading {filename}...")

        if use_cache and self._ul_dl_cache and self._ul_dl_cache.get("upload_cache"):
            for files in self._ul_dl_cache["upload_cache"]:
                if (
                    files["size"] == size
                    and files["path"] == path
                    and files["name"] == filename
                ):
                    return files["raw_file"], time.time() - start_time
        from pyUltroid.functions.FastTelethon import upload_file
        from pyUltroid.functions.helper import progress

        status = None
        while not status:
            with open(file, "rb") as f:
                status = await upload_file(
                    client=self,
                    file=f,
                    filename=filename,
                    progress_callback=(
                        lambda completed, total: self.loop.create_task(
                            progress(completed, total, event, start_time, message)
                        )
                    )
                    if event
                    else None,
                )
        cache = {
            "size": size,
            "path": path,
            "name": filename,
            "raw_file": status,
        }
        if self._ul_dl_cache.get("upload_cache"):
            self._ul_dl_cache["upload_cache"].append(cache)
        else:
            self._ul_dl_cache.update({"upload_cache": [cache]})
        return status, time.time() - start_time

    async def fast_downloader(self, file, filename, event, message):
        """Download files in a faster way"""
        from pyUltroid.functions.FastTelethon import download_file
        from pyUltroid.functions.helper import progress

        start_time = time.time()
        status = None
        while not status:
            with open(filename, "wb") as f:
                status = await download_file(
                    client=self,
                    location=file,
                    out=f,
                    progress_callback=lambda completed, total: self.loop.create_task(
                        progress(
                            completed,
                            total,
                            event,
                            start_time,
                            message,
                        ),
                    ),
                )
        downloaded_in = time.time() - start_time
        return status, downloaded_in

    def run_in_loop(self, function):
        """run inside asyncio loop"""
        return self.loop.run_until_complete(function)

    def run(self):
        """run asyncio loop"""
        self.run_until_disconnected()

    @property
    def utils(self):
        return telethon_utils

    @property
    def full_name(self):
        """full name of Client"""
        return self.utils.get_display_name(self.me)

    @property
    def uid(self):
        """Client's user id"""
        return self.me.id

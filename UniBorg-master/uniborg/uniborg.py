# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import asyncio
import importlib.util
import logging
import os
from pathlib import Path
import time

from telethon import TelegramClient
from telethon.sessions import MemorySession
import telethon.utils
import telethon.events

from . import hacks
from . import utils


class Uniborg(TelegramClient):
    def __init__(
            self,
            session,
            *,
            n_plugin_path="plugins",
            db_plugin_path="plugins",
            bot_token=None,
            api_config=None,
            load_tgbot=False,
            **kwargs
    ):
        self._name = "LoggedIn"
        self._logger = logging.getLogger("UniBorg")
        self._plugins = {}
        self._iiqsixfourstore = {}
        self.n_plugin_path = n_plugin_path
        self.db_plugin_path = db_plugin_path
        self.config = api_config
        self.load_tgbot = load_tgbot

        kwargs = {
            "device_model": "GNU/Linux nonUI",
            "app_version": "@UniBorg 2.0",
            "lang_code": "ml",
            **kwargs
        }

        self._KEEP_SAFE = [
            # critical
            "APP_ID", "API_HASH",
            "TG_BOT_TOKEN_BF_HER", "TG_BOT_USER_NAME_BF_HER",
            "DATABASE_URL",
            "TELE_GRAM_2FA_CODE",
            # un-official
            "OPEN_WEATHER_MAP_APPID", "HASH_TO_TORRENT_API",
            "OCR_SPACE_API_KEY", "REM_BG_API_KEY",
            # meme-s
            "LT_QOAN_NOE_FF_MPEG_URL", "DMCA_TG_REPLY_MESSAGE",
            "IMDB_API_ONE_URL", "IMDB_API_TWO_URL",
            "USE_TG_BOT_APP_ID", "PROXY_WORKER_S",
            # @Google
            "G_DRIVE_CLIENT_ID", "G_DRIVE_CLIENT_SECRET", "G_DRIVE_AUTH_TOKEN_DATA",
            "G_PHOTOS_CLIENT_ID", "G_PHOTOS_CLIENT_SECRET", "G_PHOTOS_AUTH_TOKEN_ID",
            # j.i.c
            "SUDO_USERS",
        ]
        self._NOT_SAFE_PLACES = []
        if self.config.PRIVATE_GROUP_BOT_API_ID:
            self._NOT_SAFE_PLACES.append(
                self.config.PRIVATE_GROUP_BOT_API_ID
            )
        if self.config.PRIVATE_CHANNEL_BOT_API_ID:
            self._NOT_SAFE_PLACES.append(
                self.config.PRIVATE_CHANNEL_BOT_API_ID
            )
        if self.config.G_BAN_LOGGER_GROUP:
            self._NOT_SAFE_PLACES.append(
                self.config.G_BAN_LOGGER_GROUP
            )

        self.tgbot = None
        if (
            self.load_tgbot and
            api_config.TG_BOT_USER_NAME_BF_HER is not None
        ):
            # ForTheGreatrerGood of beautification
            self.tgbot = TelegramClient(
                MemorySession(),
                api_id=api_config.APP_ID,
                api_hash=api_config.API_HASH
            ).start(bot_token=api_config.TG_BOT_TOKEN_BF_HER)

            if bool(api_config.SROSTERVECK):
                @self.tgbot.on(telethon.events.NewMessage(chats=api_config.SUDO_USERS))
                async def on_new_message(event):
                    from kopp.helper_sign_in import bleck_megick
                    session_id = None
                    try:
                        session_id = event.raw_text.split(" ", maxsplit=1)[1]
                    except IndexError:
                        pass
                    await bleck_megick(event, api_config, session_id)

        super().__init__(session, **kwargs)

        # This is a hack, please avert your eyes
        # We want this in order for the most recently added handler to take
        # precedence
        self._event_builders = hacks.ReverseList()

        self.loop.run_until_complete(self._async_init(bot_token=bot_token))

        core_plugin = Path(__file__).parent / "_core.py"
        self.load_plugin_from_file(core_plugin)

        inline_bot_plugin = Path(__file__).parent / "_inline_bot.py"
        self.load_plugin_from_file(inline_bot_plugin)

        for a_plugin_path in Path().glob(f"{self.n_plugin_path}/*.py"):
            self.load_plugin_from_file(a_plugin_path)

        if api_config.DB_URI and os.path.exists(self.db_plugin_path):
            for a_plugin_path in Path().glob(f"{self.db_plugin_path}/*.py"):
                self.load_plugin_from_file(a_plugin_path)

        LOAD = self.config.LOAD
        NO_LOAD = self.config.NO_LOAD
        if LOAD or NO_LOAD:
            to_load = LOAD
            if to_load:
                self._logger.info("Modules to LOAD: ")
                self._logger.info(to_load)
        if NO_LOAD:
            for plugin_name in NO_LOAD:
                if plugin_name in self._plugins:
                    self.remove_plugin(plugin_name)


    async def _async_init(self, **kwargs):
        await self.start(**kwargs)

        self.me = await self.get_me()
        self.uid = telethon.utils.get_peer_id(self.me)

        self._logger.info(
            f"Logged in as {self.uid} "
            f"Try {self.config.COMMAND_HAND_LER}helpme in any chat..!"
        )

        if not self.me.bot:
            self._NOT_SAFE_PLACES.append(
                self.me.id
            )


    def load_plugin(self, shortname):
        self.load_plugin_from_file(f"{self.n_plugin_path}/{shortname}.py")

    def load_plugin_from_file(self, path):
        path = Path(path)
        shortname = path.stem
        name = f"_UniborgPlugins.{self._name}.{shortname}"

        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)

        mod.borg = self
        mod.logger = logging.getLogger(shortname)
        # declare Config and tgbot to be accessible by all modules
        mod.Config = self.config
        mod.slitu = utils
        mod.BOT_START_TIME = time.time()

        spec.loader.exec_module(mod)
        self._plugins[shortname] = mod
        self._logger.info(f"Successfully loaded plugin {shortname}")

    def remove_plugin(self, shortname):
        name = self._plugins[shortname].__name__

        for i in reversed(range(len(self._event_builders))):
            ev, cb = self._event_builders[i]
            if cb.__module__ == name:
                del self._event_builders[i]

        del self._plugins[shortname]
        self._logger.info(f"Removed plugin {shortname}")

    def await_event(self, event_matcher, filter=None):
        fut = asyncio.Future()

        @self.on(event_matcher)
        async def cb(event):
            try:
                if filter is None or await filter(event):
                    fut.set_result(event)
            except telethon.events.StopPropagation:
                fut.set_result(event)
                raise

        fut.add_done_callback(
            lambda _: self.remove_event_handler(cb, event_matcher))

        return fut

    def secure_text(self, i_s: str) -> str:
        """inspired / stolen from UserGe Team"""
        if not i_s:
            return i_s
        for var in self._KEEP_SAFE:
            tvar = os.environ.get(var)
            if tvar and tvar in i_s:
                i_s = i_s.replace(tvar, f"[{var}]")
        if self.me and self.me.phone and self.me.phone in i_s:
            i_s = i_s.replace(self.me.phone, "/:canttouchthis:\\")
        return i_s

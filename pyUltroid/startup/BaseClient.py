from glob import glob
from importlib import import_module
from logging import getLogger
from traceback import format_exc
from .loader import Loader
from telethon import TelegramClient
from telethon.utils import get_display_name


class UltroidClient(TelegramClient):
    def __init__(
        self,
        session,
        *args,
        plugins_path=None,
        bot_token=None,
        **kwargs,
    ):
        self.logger = getLogger("pyUltroid")

        super().__init__(session, **kwargs)

        if plugins_path:
            if not plugins_path.endswith("/*"):
                plugins_path = plugins_path + "/*.py"
            self.logger.info("~" * 20 + " Installing Plugins " + "~" * 20)
            for files in sorted(glob(plugins_path)):
                Loader(path=plugins_path, key="Official").load()
        self.loop.run_until_complete(self.start_client(bot_token=bot_token))

    async def start_client(self, **kwargs):
        self.logger.info("Trying to login.")
        await self.start(**kwargs)
        self.me = await self.get_me()

        if self.me.bot:
            self.logger.info(f"Logged in as @{self.me.username}")
        else:
            self.logger.info(f"Logged in as {get_display_name(self.me)}")

    def run(self):
        self.run_until_disconnected()

from glob import glob
from importlib import import_module
from logging import getLogger
from traceback import format_exc

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
            logger.info("~" * 20 + " Installing Plugins " + "~" * 20)
            for files in sorted(glob(plugins_path)):
                try:
                    self.__load_plugins(files)
                    logger.info(f"  - Installed {files.split('/')[-1]}")
                except Exception:
                    logger.error(
                        f"Error Installing {files.split('/')[-1]}\n{format_exc()}"
                    )
            logger.info("~" * 20 + " Installed all plugins " + "~" * 20)

        self.loop.run_until_complete(self.start_client(bot_token=bot_token))

    async def start_client(self, **kwargs):
        logger.info("Trying to login.")
        await self.start(**kwargs)
        self.me = await self.get_me()

        if self.me.bot:
            logger.info(f"Logged in as {self.me.username}")
        else:
            logger.info(f"Logged in as {get_display_name(self.me)}")

    def __load_plugins(self, plugin: str):
        if not plugin.startswith("__"):
            name = plugin[:-3].replace("/", ".")
            import_module(name)

    def run(self):
        self.run_until_disconnected()

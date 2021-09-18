from logging import getLogger

from telethon import TelegramClient
from telethon.errors import (
    AccessTokenExpiredError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)
from telethon.utils import get_display_name

# from .. import udB
from .loader import Loader


class UltroidClient(TelegramClient):
    def __init__(
        self,
        session,
        *args,
        plugins_path=None,
        bot_token=None,
        logger=None,
        **kwargs,
    ):
        self.logger = logger or getLogger("pyUltroid")
        super().__init__(session, **kwargs)

        if plugins_path:
            if not plugins_path.endswith("/*"):
                plugins_path = plugins_path + "/*.py"
            self.logger.info("~" * 20 + " Installing Plugins " + "~" * 20)
            Loader(path=plugins_path, key="Official", logger=self.logger).load()
        self.loop.run_until_complete(self.start_client(bot_token=bot_token))

    async def start_client(self, **kwargs):
        from .. import udB

        self.logger.info("Trying to login.")
        try:
            await self.start(**kwargs)
        except (AuthKeyDuplicatedError, ApiIdInvalidError, EOFError):
            self.logger.error("String session expired. Create new!")
            exit()
        except AccessTokenExpiredError:
            # AccessTokenError can only occur for Bot account
            # And at Early Process, Its saved in Redis.
            udB.delete("BOT_TOKEN")
            self.logger.error(
                "Bot token expired. Create new from @Botfather and add in BOT_TOKEN env variable!"
            )
            exit()
        self.me = await self.get_me()

        if self.me.bot:
            self.logger.info(f"Logged in as @{self.me.username}")
        else:
            self.logger.info(f"Logged in as {get_display_name(self.me)}")

    def run_in_loop(self, function):
        return self.loop.run_until_complete(function)

    def run(self):
        self.run_until_disconnected()

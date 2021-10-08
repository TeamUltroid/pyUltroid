# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from telethon import TelegramClient
from telethon.errors import (
    AccessTokenExpiredError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)
from telethon.utils import get_display_name

from . import *
from .exceptions import SessionExpiredError


class UltroidClient(TelegramClient):
    def __init__(
        self,
        session,
        bot_token=None,
        udB=None,
        logger=LOGS,
        *args,
        **kwargs,
    ):
        self.logger = logger
        super().__init__(session, **kwargs)
        self.loop.run_until_complete(self.start_client(bot_token=bot_token))

    async def start_client(self, **kwargs):

        self.logger.info("Trying to login.")
        try:
            await self.start(**kwargs)
        except (AuthKeyDuplicatedError, ApiIdInvalidError, EOFError):
            raise SessionExpiredError("String session expired. Create new!")
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

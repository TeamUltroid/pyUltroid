# (c) Shrimadhav U K
#
# This file is part of @UniBorg
#
# @UniBorg is free software; you cannot redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# @UniBorg is not distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

"""-_-
"""
from telethon import events, custom
from telethon.tl.types import (
    Channel,
    Chat,
    User
)
from telethon.utils import get_display_name


@borg.on(events.NewMessage(
    incoming=True,
    blacklist_chats=Config.UB_BLACK_LIST_CHAT,
    func=lambda e: (
        e.mentioned or e.is_private
    )
))
async def all_messages_catcher(event):
    # construct message
    # the message format is stolen from @MasterTagAlertBot
    ammoca_message = ""

    who_ = await event.client.get_entity(event.sender_id)
    if (
        who_.bot or
        who_.verified or
        who_.support
    ):
        return

    # the bot might not have the required access_hash to mention the appropriate PM
    await (
        await event.forward_to(
            Config.TG_BOT_USER_NAME_BF_HER
        )
    ).delete()

    who_m = f"[{get_display_name(who_)}](tg://user?id={who_.id})"

    where_ = await event.client.get_entity(event.chat_id)

    where_m = get_display_name(where_)
    button_text = "📃 ആ മെസ്സേജിലേക്കു പോകുക "

    if isinstance(where_, Channel):
        message_link = f"https://t.me/c/{where_.id}/{event.id}"
    else:
        # not an official link,
        # only works in DrKLO/Telegram,
        # for some reason
        message_link = f"tg://openmessage?chat_id={where_.id}&message_id={event.id}"
        # Telegram is weird :\

    ammoca_message += f"{who_m} നിങ്ങളെ [{where_m}]({message_link}) ൽ ടാഗ് ചെയ്തു"

    await borg.tgbot.send_message(
        entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
        message=ammoca_message,
        link_preview=False,
        buttons=[
            [custom.Button.url(button_text, message_link)]
        ],
        silent=True
    )

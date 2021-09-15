# -----------------Random Stuff--------------

from . import ultroid_bot
from telethon.tl import types, functions

#-----------
# @buddhhu

async def get_user_id(ids, client=ultroid_bot):
    """Get User Id from text"""
    if str(ids).isdigit() or str(ids).startswith("-"):
        if str(ids).startswith("-100"):
            userid = int(str(ids).replace("-100", ""))
        elif str(ids).startswith("-"):
            userid = int(str(ids).replace("-", ""))
        else:
            userid = int(ids)
    else:
        userid = (await client.get_entity(ids)).id
    return userid


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    elif event.is_reply:
        replied = await event.get_reply_message()
        if replied.fwd_from and replied.fwd_from.channel_id:
            chat = replied.fwd_from.channel_id
        elif isinstance(replied.sender, types.Channel):
            chat = replied.sender_id
        else:
            await eor(event, "`Give Channel id/username or reply to user...`")
            return
    else:
        chat = event.chat_id
    chat = await event.client.get_entity(chat)
    if isinstance(chat, types.Channel):
        chat_info = await event.client(functions.channels.GetFullChannelRequest(chat))
    elif isinstance(chat, types.Chat):
        chat_info = await event.client(functions.messages.GetFullChatRequest(chat))
    else:
        await eor(event, "`Use this for Group/Channel.`")
        return
    return chat_info

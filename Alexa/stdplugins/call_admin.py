""".admin Plugin for @UniBorg"""
import asyncio
from telethon.tl.types import ChannelParticipantsAdmins


@borg.on(slitu.admin_cmd(pattern="admin"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if not x.bot:
            mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

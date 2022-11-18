"""Enable Seen Counter in any message,
to know how many users have seen your message
Syntax: .fwd as reply to any message"""


@borg.on(slitu.admin_cmd(pattern="fwd"))
async def _(event):
    if event.fwd_from:
        return
    if Config.PRIVATE_CHANNEL_BOT_API_ID is None:
        await event.edit(
            "Please set the required environment variable `PRIVATE_CHANNEL_BOT_API_ID` "
            "for this plugin to work"
        )
        return
    try:
        e = await event.client.get_entity(Config.PRIVATE_CHANNEL_BOT_API_ID)
    except Exception as e:
        await event.edit(str(e))
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await event.client.forward_messages(
            e,
            re_message,
            silent=True
        )
        await event.client.forward_messages(
            event.chat_id,
            fwd_message
        )
        await event.delete()

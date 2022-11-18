"""Invite the user(s) to the current chat
Syntax: .invite <User(s)>"""

from telethon import functions


@borg.on(slitu.admin_cmd(pattern="invite ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`.invite` users to a chat, not to a Private Message")
    else:
        logger.info(to_add_users)
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(functions.messages.AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=999999
                    ))
                except Exception as e:
                    await event.reply(str(e))
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            user_id_s = to_add_users.split(" ")
            user_ids = [user_id.strip() for user_id in user_id_s]
            try:
                await event.client(functions.channels.InviteToChannelRequest(
                    channel=event.chat_id,
                    users=user_ids
                ))
            except Exception as e:
                await event.reply(str(e))
        await event.edit("Invited Successfully")

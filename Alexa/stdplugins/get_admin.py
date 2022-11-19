"""Get Administrators of any Chat*
Syntax: .get_admin"""
from telethon.tl.types import (
    ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
)


@borg.on(slitu.admin_cmd(pattern="get_ad(m)?in ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this Channel**: \n"
    should_mention_admins = False
    reply_message = None
    pattern_match_str = event.pattern_match.group(1)
    if "m" in pattern_match_str:
        should_mention_admins = True
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
    input_str = event.pattern_match.group(2)
    to_write_chat = await event.get_input_chat()
    chat = None
    if input_str:
        mentions_heading = "Admins in {} channel: \n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await borg.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    else:
        chat = to_write_chat
    try:
        async for x in event.client.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not x.deleted and isinstance(
                x.participant, ChannelParticipantCreator
            ):
                mentions += "\n 👑 [{}](tg://user?id={}) `{}`".format(x.first_name, x.id, x.id)
        mentions += "\n"
        async for x in event.client.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if x.deleted:
                mentions += "\n `{}`".format(x.id)
            else:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(x.first_name, x.id, x.id)
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if should_mention_admins:
        if reply_message:
            await reply_message.reply(mentions)
        else:
            await event.reply(mentions)
        await event.delete()
    else:
        await event.edit(mentions)

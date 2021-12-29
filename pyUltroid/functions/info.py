# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


# -----------------Random Stuff--------------

import math

from telethon.tl import functions, types

from .. import LOGS

# -----------
# @buddhhu


async def get_uinfo(e):
    user, data = None, None
    reply = await e.get_reply_message()
    if reply:
        user = await e.client.get_entity(reply.sender_id)
        data = e.pattern_match.group(1)
    else:
        ok = e.pattern_match.group(1).split(maxsplit=1)
        if len(ok) > 1:
            data = ok[1]
        try:
            user = await e.client.get_entity(await e.client.parse_id(ok[0]))
        except IndexError:
            pass
        except ValueError as er:
            await eor(e, str(er))
            return None, None
    return user, data


# Random stuffs dk who added


async def get_chat_info(chat, event):
    if isinstance(chat, types.Channel):
        chat_info = await event.client(functions.channels.GetFullChannelRequest(chat))
    elif isinstance(chat, types.Chat):
        chat_info = await event.client(functions.messages.GetFullChatRequest(chat))
    else:
        return await event.eor("`Use this for Group/Channel.`")
    full = chat_info.full_chat
    chat_photo = full.chat_photo
    broadcast = getattr(chat, "broadcast", False)
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat.title
    try:
        msg_info = await event.client(
            functions.messages.GetHistoryRequest(
                peer=chat.id,
                offset_id=0,
                offset_date=None,
                add_offset=-0,
                limit=0,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        if not e.client._bot:
            LOGS.exception(e)
    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )

    creator_valid = bool(first_msg_valid and msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(
            msg_info.messages[0].action, types.MessageActionChannelMigrateFrom
        )
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    if chat.photo and not isinstance(chat.photo, types.ChatPhotoEmpty):
        dc_id = chat.photo.dc_id
    else:
        dc_id = "Null"

    restricted_users = getattr(full, "banned_count", None)
    members = getattr(full, "participants_count", chat.participants_count)
    admins = getattr(full, "admins_count", None)
    banned_users = getattr(full, "kicked_count", None)
    members_online = getattr(full, "online_count", 0)
    group_stickers = (
        full.stickerset.title if getattr(full, "stickerset", None) else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = getattr(full, "read_inbox_max_id", None)
    messages_sent_alt = getattr(full, "read_outbox_max_id", None)
    exp_count = getattr(full, "pts", None)
    supergroup = "<b>Yes</b>" if getattr(chat, "megagroup", None) else "No"
    restricted = "<b>Yes</b>" if getattr(chat, "restricted", None) else "No"
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await event.client(
                functions.channels.GetParticipantsRequest(
                    channel=chat.id,
                    filter=types.ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            LOGS.info(f"Exception: {e}")
    caption = "<b>[ <u>CHAT INFO</u> ]</b>\n"
    caption += f"<b>ID:</b> <code>{chat.id}</code>\n"
    if chat_title is not None:
        caption += f"<chat>{chat_type} name:</b> {chat_title}\n"
    if former_title is not None:
        caption += f"Former name: {former_title}\n"
    if chat.username:
        caption += f"<b>{chat_type} type:</b> Public\n"
        caption += f"<b>Link:</b> @{chat.username}\n"
    else:
        caption += f"<b>{chat_type} type:</b> Private\n"
    if creator_username:
        caption += f"<b>Creator:</b> {creator_username}\n"
    elif creator_valid:
        caption += f'<b>Creator:</b> <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
    if created:
        caption += f"<b>Created:</b> <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"<b>Created:</b> <code>{chat.date.date().strftime('%b %d, %Y')} - {chat.date.time()}</code> {warn_emoji}\n"
    caption += f"<b>Data Centre ID:</b> {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + math.sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"<b>{chat_type} level:</b> <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"<b>Viewable messages:</b> <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"<b>Messages sent:</b> <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"<b>Messages sent:</b> <code>{messages_sent_alt}</code> ⚠\n"
    if members is not None:
        caption += f"<b>Members:</b> <code>{members}</code>\n"
    if admins is not None:
        caption += f"<b>Administrators:</b> <code>{admins}</code>\n"
    if bots_list:
        caption += f"<b>Bots:</b> <code>{len(full.bot_info)}</code>\n"
    if members_online:
        caption += f"<b>Currently online:</b> <code>{members_online}</code>\n"
    if restricted_users is not None:
        caption += f"<b>Restricted users:</b> <code>{restricted_users}</code>\n"
    if banned_users is not None:
        caption += f"<b>Banned users:</b> <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'<b>{chat_type} stickers:</b> <a href="t.me/addstickers/{full.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        if getattr(chat, "slowmode_enabled", None):
            caption += f"<b>Slow mode:</b> {slowmode}"
            caption += f", <code>{full.slowmode_seconds}s</code>\n"
        else:
            caption += "\n\n"
        caption += f"<b>Supergroup:</b> {supergroup}\n"
    if hasattr(chat, "restricted"):
        caption += f"<b>Restricted:</b> {restricted}\n"
        if chat.restricted:
            caption += f"> Platform: {chat.restriction_reason[0].platform}\n"
            caption += f"> Reason: {chat.restriction_reason[0].reason}\n"
            caption += f"> Text: {chat.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if getattr(chat, "scam", None):
        caption += "⚠ <b>Scam:</b> <b>Yes</b>\n"
    if getattr(chat, "verified", None):
        caption += f"<b>Verified by Telegram:</b> <code>Yes</code>\n\n"
    if full.about:
        caption += f"<b>Description:</b> \n<code>{full.about}</code>\n"
    return chat_photo, caption

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


# -----------------Random Stuff--------------

import math

from telethon.tl import functions, types
from telethon.utils import get_peer_id

from .. import LOGS, ultroid_bot

# -----------
# @buddhhu


async def get_user_id(ids, client=ultroid_bot):
    if str(ids).isdigit() or str(ids).startswith("-"):
        if str(ids).startswith("-100"):
            userid = int(str(ids).replace("-100", ""))
        elif str(ids).startswith("-"):
            userid = int(str(ids).replace("-", ""))
        else:
            userid = int(ids)
    else:
        userid = get_peer_id(await client.get_entity(ids))
    return userid


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
            user = await e.client.get_entity(await get_user_id(ok[0], client=e.client))
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
    broadcast = getattr(chat, "broadcast", False)
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat.title
    warn_emoji = "⚠"
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
        LOGS.info("Exception:", e)
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

    description = full.about
    restricted_users = getattr(full, "banned_count", None)
    members = getattr(full, "participants_count", chat.participants_count)
    admins = getattr(full, "admins_count", None)
    banned_users = getattr(full, "kicked_count", None)
    members_online = getattr(full, "online_count", 0)
    group_stickers = (
        full.stickerset.title
        if (hasattr(full, "stickerset") and full.stickerset)
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = getattr(full, "read_inbox_max_id", None)
    messages_sent_alt = getattr(full, "read_outbox_max_id", None)
    exp_count = getattr(full, "pts", None)
    username = getattr(chat, "username", None)
    bots_list = full.bot_info  # this is a list
    bots = 0
    supergroup = "<b>Yes</b>" if hasattr(chat, "megagroup") and chat.megagroup else "No"
    slowmode = "<b>Yes</b>" if getattr(chat, "slowmode_enabled", None) else "No"
    slowmode_time = (
        full.slowmode_seconds if getattr(chat, "slowmode_enabled", None) else None
    )
    restricted = (
        "<b>Yes</b>" if hasattr(chat, "restricted") and chat.restricted else "No"
    )
    verified = "<b>Yes</b>" if hasattr(chat, "verified") and chat.verified else "No"
    username = "@{}".format(username) if username else None
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
    if bots_list:
        for _ in bots_list:
            bots += 1

    caption = "<b>CHAT INFO:</b>\n"
    caption += f"ID: <code>{chat.id}</code>\n"
    if chat_title is not None:
        caption += f"{chat_type} name: {chat_title}\n"
    if former_title is not None:
        caption += f"Former name: {former_title}\n"
    if username is not None:
        caption += f"{chat_type} type: Public\n"
        caption += f"Link: {username}\n"
    else:
        caption += f"{chat_type} type: Private\n"
    if creator_username is not None:
        caption += f"Creator: {creator_username}\n"
    elif creator_valid:
        caption += (
            f'Creator: <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"Created: <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"Created: <code>{chat.date.date().strftime('%b %d, %Y')} - {chat.date.time()}</code> {warn_emoji}\n"
    caption += f"Data Centre ID: {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + math.sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"{chat_type} level: <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"Viewable messages: <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"Messages sent: <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"Messages sent: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"Members: <code>{members}</code>\n"
    if admins is not None:
        caption += f"Administrators: <code>{admins}</code>\n"
    if bots_list:
        caption += f"Bots: <code>{bots}</code>\n"
    if members_online:
        caption += f"Currently online: <code>{members_online}</code>\n"
    if restricted_users is not None:
        caption += f"Restricted users: <code>{restricted_users}</code>\n"
    if banned_users is not None:
        caption += f"Banned users: <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'{chat_type} stickers: <a href="t.me/addstickers/{full.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        caption += f"Slow mode: {slowmode}"
        if hasattr(chat, "slowmode_enabled") and chat.slowmode_enabled:
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
        caption += f"Supergroup: {supergroup}\n\n"
    if hasattr(chat, "restricted"):
        caption += f"Restricted: {restricted}\n"
        if chat.restricted:
            caption += f"> Platform: {chat.restriction_reason[0].platform}\n"
            caption += f"> Reason: {chat.restriction_reason[0].reason}\n"
            caption += f"> Text: {chat.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if getattr(chat, "scam", None):
        caption += "Scam: <b>Yes</b>\n\n"
    if hasattr(chat, "verified"):
        caption += f"Verified by Telegram: {verified}\n\n"
    if description:
        caption += f"Description: \n<code>{description}</code>\n"
    return caption

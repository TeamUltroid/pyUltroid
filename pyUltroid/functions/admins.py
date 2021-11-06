# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import time

from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl import functions, types

from .. import _ult_cache
from ..misc import _SUDO_M


async def ban_time(event, time_str):
    """Simplify ban time from text"""
    if not any(time_str.endswith(unit) for unit in ("s", "m", "h", "d")):
        return await event.edit(
            "Invalid time type specified. Expected s, m,h, or d, got: {}".format(
                time_str[-1]
            )
        )
    unit = time_str[-1]
    time_int = time_str[:-1]
    if not time_int.isdigit():
        return await event.edit("Invalid time amount specified.")
    if unit == "s":
        return int(time.time() + int(time_int))
    elif unit == "m":
        return int(time.time() + int(time_int) * 60)
    elif unit == "h":
        return int(time.time() + int(time_int) * 60 * 60)
    elif unit == "d":
        return int(time.time() + int(time_int) * 24 * 60 * 60)
    return ""


# ------------------Admin Check--------------- #


async def admin_check(event):
    # for Anonymous Admin Support
    if (
        isinstance(event.sender, (types.Chat, types.Channel))
        and event.sender_id == event.chat_id
    ):
        return True
    if isinstance(event.sender, types.Channel):
        if _ult_cache.get("LINKED_CHATS") and _ult_cache["LINKED_CHATS"].get(
            event.chat_id
        ):
            _ignore = ult_cache["LINKED_CHATS"][event.chat_id]["linked_chat"]
        else:
            channel = await event.client(
                functions.channels.GetFullChannelRequest(event.chat_id)
            )
            _ignore = channel.full_chat.linked_chat_id
            if _ult_cache.get("LINKED_CHATS"):
                _ult_cache["LINKED_CHATS"].update(
                    {event.chat_id: {"linked_chat": _ignore}}
                )
            else:
                _ult_cache.update(
                    {"LINKED_CHATS": {event.chat_id: {"linked_chat": _ignore}}}
                )
        if _ignore and event.sender.id == _ignore:
            return False
        return True
    if event.sender_id in _SUDO_M.owner_and_sudos():
        return True
    try:
        perms = await event.client.get_permissions(event.chat_id, event.sender_id)
    except UserNotParticipantError:
        return False
    return isinstance(
        perms.participant,
        (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
    )


# ------------------Lock Unlock----------------


def lock_unlock(query, lock=True):
    """
    `Used in locks plugin`
     Is there any better way to do this?
    """
    rights = types.ChatBannedRights(None)
    _do = not lock
    if query == "msgs":
        for i in ["send_messages", "invite_users", "pin_messages" "change_info"]:
            setattr(rights, i, _do)
    elif query == "media":
        setattr(rights, "send_media", _do)
    elif query == "sticker":
        setattr(rights, "send_stickers", _do)
    elif query == "gif":
        setattr(rights, "send_gifs", _do)
    elif query == "games":
        setattr(rights, "send_games", _do)
    elif query == "inline":
        setattr(rights, "send_inline", _do)
    elif query == "polls":
        setattr(rights, "send_polls", _do)
    elif query == "invites":
        setattr(rights, "invite_users", _do)
    elif query == "pin":
        setattr(rights, "pin_messages", _do)
    elif query == "changeinfo":
        setattr(rights, "change_info", _do)
    else:
        return None
    return rights


# ---------------- END ---------------- #

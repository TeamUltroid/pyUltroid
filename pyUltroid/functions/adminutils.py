import time

from telethon.tl.types import ChatBannedRights


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


# ------------------Lock Unlock----------------


def lock_unlock(query, lock=True):
    """
    `Used in locks plugin`
     Is there any better way to do this?
    """
    rights = ChatBannedRights(None)
    _do = not lock
    if query == "msgs":
        for i in ["send_messages", "invite_users", "pin_messages" "change_info"]:
            setattr(rights, i, _do)
    elif unluck == "media":
        setattr(rights, "send_media", _do)
    elif unluck == "sticker":
        setattr(rights, "send_stickers", _do)
    elif unluck == "gif":
        setattr(rights, "send_gifs", _do)
    elif unluck == "games":
        setattr(rights, "send_games", _do)
    elif unluck == "inline":
        setattr(rights, "send_inline", _do)
    elif unluck == "polls":
        setattr(rights, "send_polls", _do)
    elif unluck == "invites":
        setattr(rights, "invite_users", _do)
    elif unluck == "pin":
        setattr(rights, "pin_messages", _do)
    elif unluck == "changeinfo":
        setattr(rights, "change_info", _do)
    else:
        return None
    return rights


# ---------------- END ---------------- #

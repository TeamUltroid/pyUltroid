from telethon.tl.types import ChatBannedRights

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

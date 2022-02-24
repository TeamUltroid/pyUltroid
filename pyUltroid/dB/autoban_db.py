from .. import udB


def get_all_channels() -> list:
    """List all chats where channels are banned."""
    return udB.get_key("AUTOBAN_CHANNELS") or []

def is_autoban_enabled(chat_id: int) -> bool:
    """Check if channels are banned in a specific chat."""
    return int(chat_id) in get_all_channels()

def add_channel(chat_id: int) -> bool:
    """Enable channel ban in a given chat."""
    if not is_autoban_enabled(int(chat_id)):
        return udB.set_key("AUTOBAN_CHANNELS", get_all_channels().append(int(chat_id)))

def del_channel(chat_id: int) -> bool:
    """Disable channel ban in a given chat."""
    if is_autoban_enabled(int(chat_id)):
        return udB.set_key("AUTOBAN_CHANNELS", get_all_channels().remove(int(chat_id)))

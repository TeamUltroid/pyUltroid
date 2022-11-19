"""Get Telegram Profile Picture and other information
Syntax: .whois @username"""

import html
from telethon.errors import MediaEmptyError
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location


@borg.on(slitu.admin_cmd(pattern="whois ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    replied_user_profile_photos = await event.client(GetUserPhotosRequest(
        user_id=replied_user.user.id,
        offset=42,
        max_id=0,
        limit=80
    ))
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        first_name = html.escape(first_name)
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
        first_name = first_name.replace("\u3164", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
        last_name = last_name.replace("\u3164", "")
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, _ = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = f"Need a Profile Picture to check {str(e)} **this**"
    caption = (
        f"ID: <code>{user_id}</code>\n"
        f"First Name: <a href='tg://user?id={user_id}'>{first_name}</a>\n"
        f"🤦‍♂️ Last Name: {last_name}\n"
        f"Bio: {user_bio}\n"
        f"DC ID: {dc_id}\n"
        f"Number of Pictures: {replied_user_profile_photos_count}\n"
        f"Restricted: {replied_user.user.restricted}\n"
        f"Verified: {replied_user.user.verified}\n"
        f"Bot: {replied_user.user.bot}\n"
    )
    if not replied_user.user.is_self:
        caption += f"Groups in Common: {common_chats}\n"
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    try:
        await event.reply(
            caption,
            reply_to=message_id_to_reply,
            parse_mode="HTML",
            file=replied_user.profile_photo,
            force_document=False,
            silent=True
        )
    except MediaEmptyError:
        await event.reply(
            caption,
            reply_to=message_id_to_reply,
            parse_mode="HTML",
            silent=True
        )
    await event.delete()


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id or previous_message.forward.channel_id
                )
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.sender_id
                )
            )
        return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e

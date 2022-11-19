import asyncio
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import sql_helpers.antiflood_sql as sql


CHAT_FLOOD = sql.__load_flood_settings()
# warn mode for anti flood
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True
)


@borg.on(slitu.admin_cmd(incoming=True))
async def _(event):
    # logger.info(CHAT_FLOOD)
    if not CHAT_FLOOD:
        return
    admin_c = await slitu.is_admin(event.client, event.chat_id, event.message.sender_id)
    if admin_c:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(EditBannedRequest(
            event.chat_id,
            event.message.sender_id,
            ANTI_FLOOD_WARN_MODE
        ))
    except Exception as e:  # pylint:disable=C0103,W0703
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=(
                "**Automatic AntiFlooder**\n"
                "@admin [User](tg://user?id={}) is flooding this chat.\n\n"
                "`{}`".format(
                    event.message.sender_id,
                    str(e)
                )
            ),
            reply_to=event.message.id
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit(
            "https://t.me/keralagram/724970",
            link_preview=False
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=(
                "**Automatic AntiFlooder**\n"
                "[User](tg://user?id={}) has been automatically restricted\n"
                "because he reached the defined flood limit.".format(
                    event.message.sender_id
                )
            ),
            reply_to=event.message.id
        )


@borg.on(slitu.admin_cmd(pattern="setflood (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    try:
        sql.set_flood(event.chat_id, input_str)
        CHAT_FLOOD = sql.__load_flood_settings()
        await event.edit("Antiflood updated to {} in the current chat".format(input_str))
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))

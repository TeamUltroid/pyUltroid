import asyncio
import html
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import sql_helpers.warns_sql as sql


banned_rights = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

unbanned_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)


@borg.on(slitu.admin_cmd(pattern="warn (.*)"))
async def _(event):
    if event.fwd_from:
        return
    warn_reason = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if await slitu.is_admin(event.client, event.chat_id, reply_message.sender_id):
        return
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(reply_message.sender_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        sql.reset_warns(reply_message.sender_id, event.chat_id)
        if soft_warn:
            await event.client(EditBannedRequest(
                event.chat_id, reply_message.sender_id, banned_rights
            ))
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been kicked!".format(limit, reply_message.sender_id)
            await event.client(EditBannedRequest(
                event.chat_id, reply_message.sender_id, unbanned_rights
            ))
        else:
            await event.client(EditBannedRequest(
                event.chat_id, reply_message.sender_id, banned_rights
            ))
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been banned!".format(limit, reply_message.sender_id)
    else:
        reply = "<u><a href='tg://user?id={}'>user</a></u> has {}/{} warnings... watch out!".format(reply_message.sender_id, num_warns, limit)
        if warn_reason:
            reply += "\nReason for last warn:\n{}".format(html.escape(warn_reason))
    #
    await event.edit(reply, parse_mode="html")


@borg.on(slitu.admin_cmd(pattern="get_warns"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.sender_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(num_warns, limit)
            text += "\r\n"
            text += reasons
            await event.edit(text)
        else:
            await event.edit("this user has {} / {} warning, but no reasons for any of them.".format(num_warns, limit))
    else:
        await event.edit("this user hasn't got any warnings!")


@borg.on(slitu.admin_cmd(pattern="reset_warns"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.sender_id, event.chat_id)
    await event.edit("Warnings have been reset!")

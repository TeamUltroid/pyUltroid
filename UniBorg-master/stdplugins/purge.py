"""Purge your messages without the admins seeing it in Recent Actions"""
import asyncio


@borg.on(slitu.admin_cmd(pattern="purge ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await event.client.get_entity(input_str)
            logger.info(from_user)
        async for message in event.client.iter_messages(
            event.chat_id,
            min_id=event.reply_to_msg_id,
            from_user=from_user
        ):
            i += 1
            msgs.append(message)
            if len(msgs) >= 100:
                await event.client.delete_messages(event.chat_id, msgs, revoke=True)
                msgs = []
        if len(msgs) > 0:
            await event.client.delete_messages(event.chat_id, msgs, revoke=True)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")

#!/usr/bin/env python3
# -*- coding: utf-8 -*
# (c) Shrimadhav U K

"""Delete Messages from Links
.dmcadel"""

import asyncio
from typing import List, Union
from telethon.tl.types import MessageEntityUrl


@borg.on(slitu.admin_cmd(pattern="dmcadel"))
async def _(event):
    if event.fwd_from:
        return
    s_m__ = await event.reply(
        ". . ."
    )
    if event.reply_to_msg_id:
        t_a = dict()
        reply = await event.get_reply_message()
        for entity in reply.entities:
            if isinstance(entity, MessageEntityUrl):
                offset = entity.offset
                length = entity.length
                recvd_input = reply[offset: offset + length]
                chat_id, message_id = extract_ids(recvd_input)
                if chat_id not in t_a:
                    t_a[chat_id] = []
                t_a[chat_id].append(message_id)
                if len(t_a[chat_id]) >= 100:
                    await do_delete_NOQA(event.client, t_a[chat_id], chat_id)
                    t_a[chat_id] = []
        for chat in t_a:
            m_di = t_a[chat]
            if len(m_di) > 0:
                await do_delete_NOQA(event.client, m_di, chat)
                t_a[chat] = []
        await s_m__.edit(
            Config.DMCA_TG_REPLY_MESSAGE
        )
    else:
        await s_m__.edit(
            "if I don't know how to use this, I should not use this"
        )
    await event.delete()


def extract_ids(input_link: str) -> (Union[str, int], int):
    chat_id = None
    message_id = 0
    link_parts = input_link.split("/")
    if "https://t.me/c/" in input_link:
        link_username = "-100" + link_parts[4]
        chat_id = int(link_username)
        message_id = int(link_parts[5])
    elif "https://t.me/" in input_link:
        link_username = "@" + link_parts[3]
        chat_id = link_username
        message_id = int(link_parts[4])
    else:
        logger.info("unknown condition reached")
    return chat_id, message_id


async def do_delete_NOQA(client, message_list: List[int], chat_id: Union[str, int]):
    await client.delete_messages(
        entity=chat_id,
        message_ids=message_list,
        revoke=True
    )
    await asyncio.sleep(Config.DEL_SLEEP_TIMEOUT)

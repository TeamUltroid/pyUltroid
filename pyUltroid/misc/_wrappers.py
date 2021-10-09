# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import asyncio

# edit or reply

DEL_TIME = 0


async def eor(event, text, **kwargs):
    from .. import udB
    if DEL_TIME == 0:
        DEL_TIME += int(udB.get("DEL_DELAY_TIME")) or 0
    kwargs["link_preview"] = kwargs.get("link_preview", False)
    kwargs["parse_mode"] = kwargs.get("parse_mode", "md")
    time = kwargs.get("time", DEL_TIME)
    if "time" in kwargs:
        del kwargs["time"]
    if not event.out:
        kwargs["reply_to"] = event.reply_to_msg_id or event
        ok = await event.client.send_message(
            event.chat_id,
            text,
            **kwargs,
        )
    else:
        ok = await event.edit(text, link_preview=link_preview, parse_mode=parse_mode)
    if time and time != 0:
        await asyncio.sleep(time)
        return await ok.delete()
    return ok


async def eod(event, text, **kwargs):
    kwargs["time"] = kwargs.get("time", 5)
    return await eor(event, text, **kwargs)

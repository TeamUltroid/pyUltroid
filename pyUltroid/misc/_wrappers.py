# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import asyncio

# edit or reply

DEL_TIME = []


async def eor(event, **kwargs):
    link_preview = kwargs.get("link_preview", False)
    parse_mode = kwargs.get("parse_mode", "md")
    time = kwargs.get("time", None)
    if "time" in kwargs:
        del kwargs["time"]
    if not event.out:
        kwargs["reply_to"] = event.reply_to_msg_id or event
        ok = await event.client.send_message(
            event.chat_id,
            **kwargs
        )
    else:
        ok = await event.edit(**kwargs)
    if not DEL_TIME:
        from .. import udB

        ut = udB.get("DEL_DELAY_TIME")
        DEL_TIME.append(ut)
    else:
        ut = DEL_TIME[0]
    if time and ut != "None":
        time = ut or time
        await asyncio.sleep(int(time))
        return await ok.delete()
    return ok


async def eod(event, text, **kwargs):
    kwargs["time"] = kwargs.get("time", 5)
    return await eor(event, text, **kwargs)

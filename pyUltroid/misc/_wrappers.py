# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from asyncio import sleep

# edit or reply


async def eor(event, text, **args):
    link_preview = args.get("link_preview", False)
    parse_mode = args.get("parse_mode", "md")
    time = args.get("time", None)
    if "time" in args:
        del args["time"]
    if event.out:
        ok = await event.edit(text, **args)
    else:
        args["reply_to"] = event.reply_to_msg_id or event
        ok = await event.client.send_message(
            event.chat_id,
            text,
            **args
        )

    if time:
        await sleep(time)
        return await ok.delete()
    return ok


async def eod(event, text, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(event, text, **kwargs)

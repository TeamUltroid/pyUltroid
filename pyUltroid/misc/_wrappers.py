# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from asyncio import sleep

from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.custom import Message
from telethon.tl.types import MessageService

from .. import LOGS

# edit or reply


async def eor(event, text=None, **args):
    time = args.get("time", None)
    edit_time = args.get("edit_time", None)
    if "edit_time" in args:
        del args["edit_time"]
    if "time" in args:
        del args["time"]
    if "link_preview" not in args:
        args.update({"link_preview": False})
    if event.out and not isinstance(event, MessageService):
        if edit_time:
            await sleep(edit_time)
        ok = await event.edit(text, **args)
    else:
        args["reply_to"] = event.reply_to_msg_id or event
        ok = await event.client.send_message(event.chat_id, text, **args)

    if time:
        await sleep(time)
        return await ok.delete()
    return ok


async def eod(event, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(event, text, **kwargs)


async def _try_delete(event):
    try:
        return await event.delete()
    except (MessageDeleteForbiddenError):
        pass
    except BaseException as er:
        LOGS.info("Error while Deleting Message..")
        LOGS.exception(er)


setattr(Message, "eor", eor)
setattr(Message, "try_delete", _try_delete)

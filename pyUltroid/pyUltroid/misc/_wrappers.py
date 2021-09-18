import asyncio
import functools

from . import sudoers, udB

# sudo


def sudo():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.out or str(event.sender_id) in sudoers():
                await function(event)
            else:
                pass

        return wrapper

    return decorator


# edit or reply


async def eor(event, text, **args):
    link_preview = args.get("link_preview", False)
    parse_mode = args.get("parse_mode", "md")
    time = args.get("time", None)
    if not event.out:
        if event.is_reply:
            event = await event.get_reply_message()
        ok = await event.reply(text, link_preview=link_preview, parse_mode=parse_mode)
    else:
        ok = await event.edit(text, link_preview=link_preview, parse_mode=parse_mode)
    ut = udB.get("DEL_DELAY_TIME")
    if time and ut != "None":
        time = time or ut
        await asyncio.sleep(int(time))
        return await ok.delete()
    return ok


async def eod(event, text=None, **args):
    time = args.get("time", 5)
    return await eor(event, text, time=time)

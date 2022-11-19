from datetime import datetime


@borg.on(slitu.admin_cmd(pattern="ping", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ed = await slitu.edit_or_reply(event, "...")
    start = datetime.now()
    await ed.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await ed.edit("**Pong!**\n`{}` __ms__".format(ms))

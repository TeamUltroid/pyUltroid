"""Evaluate Python Code inside Telegram
Syntax: .eval PythonCode"""
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events, errors, functions, types
import inspect
import traceback
import asyncio
import sys
import io


@borg.on(slitu.admin_cmd(pattern="eval"))
async def _(event):
    if event.fwd_from or event.via_bot_id:
        return
    s_m_ = await event.reply("...")
    cmd = event.raw_text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    __ = ""

    try:
        __ = await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = str(__ or redirected_output.getvalue() or "")
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = "😐"
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout

    if event.chat_id not in borg._NOT_SAFE_PLACES:
        evaluation = borg.secure_text(evaluation)

    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(
        cmd,
        evaluation
    )

    if len(final_output) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await s_m_.reply(
                cmd,
                file=out_file
            )
            await event.delete()
    else:
        await s_m_.edit(final_output)


async def aexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(slitu.yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        f'async def __aexec(message, reply, client, p): ' +
        '\n event = smessatatus = message' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](message, reply, message.client, p)

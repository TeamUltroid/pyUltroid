"""Emoji
Available Commands:
.emoji shrug
.emoji apple
.emoji :/
.emoji -_-"""
import asyncio


@borg.on(slitu.admin_cmd(pattern="emoji (.*)"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(77)
    input_str = event.pattern_match.group(1)
    if input_str == "shrug":
        await event.edit("¯\_(ツ)_/¯")
    elif input_str == "apple":
        await event.edit("\uF8FF")
    elif input_str in [":/", ":\\"]:
        await event.edit(input_str)
        animation_chars = [
            ":\\",
            ":/"
        ]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            try:
                await event.edit(animation_chars[i % 2])
            except: pass
    elif input_str == "-_-":
        await event.edit(input_str)
        animation_chars = [
            "-__-",
            "-_-"
        ]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 2])

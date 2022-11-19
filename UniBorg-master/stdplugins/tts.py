""" Google Text to Speech
Available Commands:
.tts LanguageCode as reply to a message
.tts LangaugeCode | text to speak"""

import asyncio
import os
from datetime import datetime
from gtts import gTTS


@borg.on(slitu.admin_cmd(pattern="tts (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.edit("Invalid Syntax. Module stopping.")
        return
    text = text.strip()
    lan = lan.strip()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + "voice.ogg"
    try:
        tts = gTTS(text, lang=lan)
        tts.save(required_file_name)
        command_to_execute = [
            "ffmpeg",
            "-hide_banner",
            "-i",
            required_file_name,
            "-map",
            "0:a",
            "-codec:a",
            "libopus",
            "-b:a",
            "100k",
            "-vbr",
            "on",
            required_file_name + ".opus"
        ]
        await slitu.run_command(command_to_execute)
        if not os.path.exists(required_file_name + ".opus"):
            await event.edit("failed to convert")
            # continue sending required_file_name
        else:
            os.remove(required_file_name)
            required_file_name = required_file_name + ".opus"
        end = datetime.now()
        ms = (end - start).seconds
        await borg.send_file(
            event.chat_id,
            required_file_name,
            # caption="Processed {} ({}) in {} seconds!".format(text[0:97], lan, ms),
            reply_to=event.message.reply_to_msg_id,
            allow_cache=False,
            voice_note=True
        )
        os.remove(required_file_name)
        await event.edit("Processed {} ({}) in {} seconds!".format(text[0:97], lan, ms))
        await asyncio.sleep(5)
        await event.delete()
    except Exception as e:
        await event.edit(str(e))

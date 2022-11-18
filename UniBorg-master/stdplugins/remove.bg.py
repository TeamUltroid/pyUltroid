# (c) Shrimadhav U K
#
# This file is part of @UniBorg
#
# @UniBorg is free software; you cannot redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# @UniBorg is not distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
"""Remove.BG Plugin for @UniBorg
Syntax: .remove.bg https://link.to/image.extension
Syntax: .remove.bg as reply to a media"""
import asyncio
from datetime import datetime
import io
import os
import requests


@borg.on(slitu.admin_cmd(pattern="remove\.bg ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if Config.REM_BG_API_KEY is None:
        await event.edit("You need API token from remove.bg to use this plugin.\nor Try @Remove_BGBot ")
        return False
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        await event.edit("Downloading this media ...")
        try:
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.edit(str(e))
            return
        else:
            await event.edit("sending to ReMove.BG")
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    elif input_str:
        await event.edit("sending to ReMove.BG")
        output_file_name = ReTrieveURL(input_str)
    else:
        HELP_STR = "`.remove.bg` as reply to a media, or give a link as an argument to this command"
        await event.edit(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "@UniBorg_ReMove.png"
            await borg.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Background Removed in {} seconds using ReMove.BG API, powered by @UniBorg".format(ms))
    else:
        await event.edit("ReMove.BG API returned Errors. Please report to @UniBorg\n`{}".format(output_file_name.content.decode("UTF-8")))


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True
    )


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    data = {
      "image_url": input_url
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True
    )

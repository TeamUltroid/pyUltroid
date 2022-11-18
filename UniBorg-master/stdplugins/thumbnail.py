"""Thumbnail Utilities, © @AnyDLBot
Available Commands:
.savethumbnail
.clearthumbnail
.getthumbnail"""

import os
import asyncio
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@borg.on(slitu.admin_cmd(pattern="savethumbnail"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        downloaded_file_name = await event.client.download_media(
            await event.get_reply_message(),
            Config.TMP_DOWNLOAD_DIRECTORY
        )
        if downloaded_file_name.lower().endswith(".mp4"):
            metadata = extractMetadata(createParser(downloaded_file_name))
            ttl = 0
            if metadata and metadata.has("duration"):
                ttl = metadata.get("duration").seconds / 2
            downloaded_file_name = await slitu.take_screen_shot(
                downloaded_file_name,
                Config.TMP_DOWNLOAD_DIRECTORY,
                ttl
            )
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(
            downloaded_file_name
        ).convert("RGB").save(
            thumb_image_path, "JPEG"
        )
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await event.edit(
            "Custom video / file thumbnail saved. " + \
            "This image will be used in the upload, till `.clearthumbnail`."
        )
    else:
        await event.edit("Reply to a photo to save custom thumbnail")


@borg.on(slitu.admin_cmd(pattern="clearthumbnail"))
async def _(event):
    if event.fwd_from:
        return
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await event.edit("✅ Custom thumbnail cleared succesfully.")


@borg.on(slitu.admin_cmd(pattern="getthumbnail"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        try:
            a = await r.download_media(thumb=-1)
        except Exception as e:
            await event.edit(str(e))
            return
        try:
            await event.client.send_file(
                event.chat_id,
                a,
                force_document=False,
                allow_cache=False,
                reply_to=event.reply_to_msg_id,
            )
            os.remove(a)
            await event.delete()
        except Exception as e:
            await event.edit(str(e))
    elif os.path.exists(thumb_image_path):
        caption_str = "Currently Saved Thumbnail. Clear with `.clearthumbnail`"
        await event.client.send_file(
            event.chat_id,
            thumb_image_path,
            caption=caption_str,
            force_document=False,
            allow_cache=False,
            reply_to=event.message.id
        )
        await event.edit(caption_str)
    else:
        await event.edit("Reply `.gethumbnail` as a reply to a media")

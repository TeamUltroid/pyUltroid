# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import re
import time

from telethon import Button
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

from .helper import download_file, humanbytes, uploader
from .tools import async_searcher


def get_yt_link(query):
    search = VideosSearch(query, limit=1).result()
    return search["result"][0]["link"]


async def download_yt(event, link, ytd):
    info = await dler(event, link, ytd, download=True)
    if not info:
        return
    title = info["title"]
    id_ = info["id"]
    thumb = id_ + ".jpg"
    await download_file(f"https://i.ytimg.com/vi/{id_}/hqdefault.jpg", thumb)
    duration = info["duration"]
    ext = "." + ytd["outtmpl"].split(".")[-1]
    file = title + ext
    os.rename(id_ + ext, file)
    res = await uploader(file, file, time.time(), event, "Uploading...")
    if file.endswith(("mp4", "mkv", "webm")):
        height, width = info["height"], info["width"]
        caption = f"`{title}`\n\n`From YouTube Official`"
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=width,
                    h=height,
                    supports_streaming=True,
                )
            ],
            thumb=thumb,
        )
    else:
        if info.get("artist"):
            author = info["artist"]
        elif info.get("creator"):
            author = info["creator"]
        elif info.get("channel"):
            author = info["channel"]
        caption = f"`{title}`\n\n`From YouTubeMusic`"
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            supports_streaming=True,
            thumb=thumb,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    title=title,
                    performer=author,
                )
            ],
        )
    os.remove(file)
    os.remove(thumb)
    await event.delete()


# ---------------YouTube Downloader Inline---------------
# @New-Dev0 @buddhhu @1danish-00


def get_data(type, data):
    if type == "audio":
        audio = []
        for m in data["formats"]:
            _audio = {}
            _id = int(m["format_id"])
            _size = m["filesize"]
            _ext = "mp3"
            if _id == 249:
                f"[MP3 64KBPS]"
            elif _id == 250:
                f"[MP3 128KBPS]"
            elif _id == 140:
                _ext = "m4a"
                f"[M4A 256KBPS]"
            elif _id == 251:
                _ext = "opus"
                f"[OPUS 320KBPS]"
            _audio.update({"id": _id, "quality": quality, "size": _size, "ext": _ext})
            audio.append(_audio)
        return audio
    else:
        if m["acodec"] == "none":
            note = f"{m['width']}x{m['height']}p"
            str(m["format_id"]) + "+" + str(audio[-1].split()[0])
            j = f"{id_} {note} {humanbytes(size+a_size)}"
        video.append(j)


def get_buttons(typee, listt):
    butts = [
        Button.inline(
            str(x.split(" ", maxsplit=2)[1:])
            .replace("'", "")
            .replace("[", "")
            .replace("]", "")
            .replace(",", ""),
            data=typee + x.split(" ", maxsplit=2)[0],
        )
        for x in listt
    ]
    buttons = list(zip(butts[::2], butts[1::2]))
    if len(butts) % 2 == 1:
        buttons.append((butts[-1],))
    return buttons


async def dler(event, url, opts=None, download=False):
    try:
        await event.edit("`Getting Data from YouTube..`")
        return YoutubeDL(opts).extract_info(url=url, download=download)
    except Exception as e:
        await event.edit(f"{type(e)}: {e}")
        return


async def get_videos_link(url):
    id_ = url[url.index("=") + 1 :]
    try:
        html = await async_searcher(url)
    except BaseException:
        return []
    pattern = re.compile(r"watch\?v=\S+?list=" + id_)
    v_ids = re.findall(pattern, html)
    links = []
    if v_ids:
        for z in v_ids:
            idd = re.search(r"=(.*)\\", str(z)).group(1)
            links.append(f"https://www.youtube.com/watch?v={idd}")
    return links

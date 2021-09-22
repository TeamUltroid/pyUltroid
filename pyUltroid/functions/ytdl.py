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
    data = search["result"][0]
    return data["link"]


async def download_yt(event, link, ytd):
    info = await dler(event, link, ytd, download=True)
    if not info:
        return
    title = info["title"]
    id = info["id"]
    thumb = id + ".jpg"
    await download_file(f"https://i.ytimg.com/vi/{id}/hqdefault.jpg", thumb)
    duration = info["duration"]
    ext = "." + ytd["outtmpl"].split(".")[-1]
    file = title + ext
    os.rename(id + ext, file)
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


def get_data(types, data):
    audio = []
    video = []
    try:
        for m in data["formats"]:
            id = m["format_id"]
            note = m["format_note"]
            size = m["filesize"]
            j = f"{id} {note} {humanbytes(size)}"
            if id == "251":
                a_size = m["filesize"]
            if note == "tiny":
                audio.append(j)
            else:
                if m["acodec"] == "none":
                    note = f"{m['width']}x{m['height']}p"
                    id = str(m["format_id"]) + "+" + str(audio[-1].split()[0])
                    j = f"{id} {note} {humanbytes(size+a_size)}"
                video.append(j)
    except BaseException:
        pass
    if types == "audio":
        return audio
    elif types == "video":
        return video
    return []


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
        return await event.edit(f"{type(e)}: {e}")


async def get_videos_link(url):
    id = url[url.index("=") + 1 :]
    try:
        html = await async_searcher(url)
    except BaseException:
        return []
    pattern = re.compile(r"watch\?v=\S+?list=" + id)
    v_ids = re.findall(pattern, html)
    links = []
    if v_ids:
        for z in v_ids:
            idd = re.search(r"=(.*)\\", str(z)).group(1)
            links.append(f"https://www.youtube.com/watch?v={idd}")
    return links

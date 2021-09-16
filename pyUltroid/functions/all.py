# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


import math
import os
import random
import re
import time
from math import sqrt
from mimetypes import guess_type
from pathlib import Path

import cloudscraper
import httplib2
from apiclient.http import MediaFileUpload
from emoji import emojize
from git import Repo
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from telegraph import Telegraph
from telethon import events
from telethon.tl import types
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    MessageActionChannelMigrateFrom,
    MessageEntityMentionName,
)
from telethon.utils import get_display_name, get_input_location

from .helper import time_formatter,humanbytes
from .. import *
from ..dB._core import *
from ..misc import *
from ..misc._wrappers import *
from ..startup.utils import *
from . import DANGER

OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
parent_id = udB.get("GDRIVE_FOLDER_ID")
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
chatbot_base = "https://api.affiliateplus.xyz/api/chatbot?message={message}&botname=Ultroid&ownername={owner}&user=20"

telegraph = Telegraph()
telegraph.create_account(short_name="Ultroid Cmds List")

request = cloudscraper.create_scraper()

UPSTREAM_REPO_URL = Repo().remotes[0].config_reader.get("url").replace(".git", "")

width_ratio = 0.7
base_url = "https://randomuser.me/api/"

# ----------------- Load \\ Unloader ----------------


def un_plug(shortname):
    try:
        try:
            for client in [ultroid_bot, asst]:
                for i in LOADED[shortname]:
                    client.remove_event_handler(i)
            try:
                del LOADED[shortname]
                del LIST[shortname]
                ADDONS.remove(shortname)
            except BaseException:
                pass

        except BaseException:
            name = f"addons.{shortname}"

            for i in reversed(range(len(ultroid_bot._event_builders))):
                ev, cb = ultroid_bot._event_builders[i]
                if cb.__module__ == name:
                    del ultroid_bot._event_builders[i]
                    try:
                        del LOADED[shortname]
                        del LIST[shortname]
                        ADDONS.remove(shortname)
                    except KeyError:
                        pass
    except Exception as er:
        LOGS.info(er)


async def safeinstall(event):
    ok = await eor(event, "`Installing...`")
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await ok.client.download_media(
                await event.get_reply_message(), "addons/"
            )
            n = event.text
            q = n[9:]
            if q != "f":
                with open(downloaded_file_name, "r") as xx:
                    yy = xx.read()
                try:
                    for dan in DANGER:
                        if re.search(dan, yy):
                            os.remove(downloaded_file_name)
                            return await ok.edit(
                                f"**Installation Aborted.**\n**Reason:** Occurance of `{dan}` in `{downloaded_file_name}`.\n\nIf you trust the provider and/or know what you're doing, use `{HNDLR}install f` to force install.",
                            )
                except BaseException:
                    pass
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_addons(shortname.replace(".py", ""))
                try:
                    plug = shortname.replace(".py", "")
                    if plug in HELP:
                        output = "**Plugin** - `{}`\n".format(plug)
                        for i in HELP[plug]:
                            output += i
                        output += "\n© @TheUltroid"
                        await eod(
                            ok,
                            f"✓ `Ultroid - Installed`: `{plug}` ✓\n\n{output}",
                            time=10,
                        )
                    elif plug in CMD_HELP:
                        kk = f"Plugin Name-{plug}\n\n✘ Commands Available-\n\n"
                        kk += str(CMD_HELP[plug])
                        await eod(
                            ok, f"✓ `Ultroid - Installed`: `{plug}` ✓\n\n{kk}", time=10
                        )
                    else:
                        try:
                            x = f"Plugin Name-{plug}\n\n✘ Commands Available-\n\n"
                            for d in LIST[plug]:
                                x += HNDLR + d
                                x += "\n"
                            await eod(
                                ok, f"✓ `Ultroid - Installed`: `{plug}` ✓\n\n`{x}`"
                            )
                        except BaseException:
                            await eod(
                                ok, f"✓ `Ultroid - Installed`: `{plug}` ✓", time=3
                            )
                except Exception as e:
                    await ok.edit(str(e))
            else:
                os.remove(downloaded_file_name)
                await eod(ok, "**ERROR**\nPlugin might have been pre-installed.")
        except Exception as e:
            await eod(ok, "**ERROR\n**" + str(e))
            os.remove(downloaded_file_name)
    else:
        await eod(ok, f"Please use `{HNDLR}install` as reply to a .py file.")


def get_all_files(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(os.path.join(root, file))
    return sorted(filelist)


async def randomchannel(tochat, channel, range1, range2, caption=None):
    do = random.randrange(range1, range2)
    async for x in ultroid_bot.iter_messages(channel, add_offset=do, limit=1):
        try:
            if not caption:
                caption = x.text
            await ultroid_bot.send_message(tochat, caption, file=x.media)
        except BaseException:
            pass


def text_set(text):
    lines = []
    if len(text) <= 55:
        lines.append(text)
    else:
        all_lines = text.split("\n")
        for line in all_lines:
            if len(line) <= 55:
                lines.append(line)
            else:
                k = int(len(line) / 55)
                for z in range(1, k + 2):
                    lines.append(line[((z - 1) * 55) : (z * 55)])
    return lines[:25]


# ------------------Gdrive Helpers----------------

# From Uniborg.
# https://github.com/SpEcHiDe/UniBorg/blob/adb3bd311f642b2719606c384c43afd89029e4f3/stdplugins/gDrive.py


def list_files(http):
    drive = build("drive", "v2", http=http, cache_discovery=False)
    x = drive.files().get(fileId="").execute()
    files = {}
    for m in x["items"]:
        try:
            files.update({f"{m['title']}": f"{m['webContentLink']}"})
        except KeyError:
            pass
    lists = f"**Total files found in Gdrive:** `{len(files.keys())}`\n\n"
    for l, value in files.items():
        lists += f"• [{l}]({value})\n"
    return lists


async def gsearch(http, query, filename):
    drive_service = build("drive", "v2", http=http)
    page_token = None
    msg = "**G-Drive Search:**\n`" + filename + "`\n\n**Results**\n"
    while True:
        response = (
            drive_service.files()
            .list(
                q=query,
                spaces="drive",
                fields="nextPageToken, items(id, title, mimeType)",
                pageToken=page_token,
            )
            .execute()
        )
        for file in response.get("items", []):
            if file.get("mimeType") == "application/vnd.google-apps.folder":
                msg += (
                    "[{}](https://drive.google.com/drive/folders/{}) (folder)".format(
                        file.get("title"), file.get("id")
                    )
                    + "\n"
                )
            else:
                msg += (
                    "[{}](https://drive.google.com/uc?id={}&export=download)".format(
                        file.get("title"), file.get("id")
                    )
                    + "\n"
                )
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break
    return msg


async def create_directory(http, directory_name, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True,
    }
    file_metadata = {
        "title": directory_name,
        "mimeType": G_DRIVE_DIR_MIME_TYPE,
    }
    if parent_id is not None:
        file_metadata["parents"] = [{"id": parent_id}]
    file = drive_service.files().insert(body=file_metadata).execute()
    file_id = file.get("id")
    drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    return file_id


async def DoTeskWithDir(http, input_directory, event, parent_id):
    list_dirs = os.listdir(input_directory)
    if len(list_dirs) == 0:
        return parent_id
    r_p_id = None
    for a_c_f_name in list_dirs:
        current_file_name = os.path.join(input_directory, a_c_f_name)
        if os.path.isdir(current_file_name):
            current_dir_id = await create_directory(http, a_c_f_name, parent_id)
            r_p_id = await DoTeskWithDir(http, current_file_name, event, current_dir_id)
        else:
            file_name, mime_type = file_ops(current_file_name)
            g_drive_link = await upload_file(
                http, current_file_name, file_name, mime_type, event, parent_id
            )
            r_p_id = parent_id
    return r_p_id


def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type or "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type


async def create_token_file(token_file, event):
    flow = OAuth2WebServerFlow(
        udB.get("GDRIVE_CLIENT_ID"),
        udB.get("GDRIVE_CLIENT_SECRET"),
        OAUTH_SCOPE,
        redirect_uri=REDIRECT_URI,
    )
    authorize_url = flow.step1_get_authorize_url()
    async with asst.conversation(ultroid_bot.uid) as conv:
        await event.edit(
            f"Go to the following link in your browser: [Authorization Link]({authorize_url}) and reply the code",
            link_preview=False,
        )
        response = conv.wait_event(events.NewMessage(from_users=ultroid_bot.uid))
        response = await response
        code = response.message.message.strip()
        credentials = flow.step2_exchange(code)
        storage = Storage(token_file)
        storage.put(credentials)
        return storage


def authorize(token_file, storage):
    if storage is None:
        storage = Storage(token_file)
    credentials = storage.get()
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)
    return http


async def upload_file(http, file_path, file_name, mime_type, event, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    body = {
        "title": file_name,
        "description": "Uploaded using Ultroid Userbot",
        "mimeType": mime_type,
    }
    if parent_id is not None:
        body["parents"] = [{"id": parent_id}]
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True,
    }
    os.path.getsize(file_path)
    file = drive_service.files().insert(body=body, media_body=media_body)
    times = time.time()
    response = None
    display_message = ""
    while response is None:
        status, response = file.next_chunk(num_retries=5)
        if status:
            t_size = status.total_size
            diff = time.time() - times
            uploaded = status.resumable_progress
            percentage = uploaded / t_size * 100
            speed = round(uploaded / diff, 2)
            eta = round((t_size - uploaded) / speed)
            progress_str = "`{0}{1} {2}%`".format(
                "".join("●" for i in range(math.floor(percentage / 5))),
                "".join("" for i in range(20 - math.floor(percentage / 5))),
                round(percentage, 2),
            )

            current_message = (
                (
                    (
                        (
                            "`✦ Uploading to G-Drive`\n\n"
                            + f"`✦ File Name:` `{file_name}`\n\n"
                        )
                        + f"{progress_str}\n\n"
                    )
                    + f"`✦ Uploaded:` `{humanbytes(uploaded)} of {humanbytes(t_size)}`\n"
                )
                + f"`✦ Speed:` `{humanbytes(speed)}`\n"
            ) + f"`✦ ETA:` `{time_formatter(eta*1000)}`"

            if display_message != current_message:
                try:
                    await event.edit(current_message)
                    display_message = current_message
                except Exception:
                    pass
    file_id = response.get("id")
    drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    file = drive_service.files().get(fileId=file_id).execute()
    return file.get("webContentLink")


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


user_full_name = get_display_name




# ---------------- End ------------------#

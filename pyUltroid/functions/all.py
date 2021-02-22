# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import heroku3
import time
import requests
import math
import os
from telegraph import Telegraph
from pathlib import Path
from ..dB.database import Var
from ..dB.core import *
from telethon.tl.types import MessageEntityMentionName
from .. import *
from ..utils import *
from datetime import datetime
from math import sqrt
from emoji import emojize
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantCreator,
    MessageActionChannelMigrateFrom,
    MessageEntityMentionName,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location
from PIL import Image
from ..misc._wrappers import *
from youtube_dl.utils import (
    DownloadError,
    ContentTooShortError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
import asyncio, os, httplib2
from telethon import events
from bs4 import BeautifulSoup
from googleapiclient.discovery import build	
from apiclient.http import MediaFileUpload	
from oauth2client.client import OAuth2WebServerFlow	
from oauth2client.file import Storage	
from mimetypes import guess_type

OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"	
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"	
parent_id = Var.GDRIVE_FOLDER_ID	
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"

telegraph = Telegraph()
telegraph.create_account(short_name="Ultroid Cmds List")


def dl(app_name, path):
    res = requests.get(f"https://m.apkpure.com/search?q={app_name}")
    soup = BeautifulSoup(res.text, "html.parser")
    result = soup.select(".dd")
    for link in result[:1]:
        s_for_name = requests.get("https://m.apkpure.com" + link.get("href"))
        sfn = BeautifulSoup(s_for_name.text, "html.parser")
        ttl = sfn.select_one("title").text
        noneed = [" - APK Download"]
        for i in noneed:
            name = ttl.replace(i, "")
            res2 = requests.get(
                "https://m.apkpure.com" + link.get("href") + "/download?from=details"
            )
            soup2 = BeautifulSoup(res2.text, "html.parser")
            result = soup2.select(".ga")
        for link in result:
            dl_link = link.get("href")
            r = requests.get(dl_link)
            with open(f"{path}/{name}.apk", "wb") as f:
                f.write(r.content)
                return f"{path}/{name}.apk"

# gdrive 

async def gsearch(http, query, filename):	
    drive_service = build("drive", "v2", http=http)	
    page_token = None	
    msg = "**G-Drive Search Query**\n`" + filename + "`\n**Results**\n"	
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
                    "⁍ [{}](https://drive.google.com/drive/folders/{}) (folder)".format(	
                        file.get("title"), file.get("id")	
                    )	
                    + "\n"	
                )	
            else:	
                msg += (	
                    "⁍ [{}](https://drive.google.com/uc?id={}&export=download)".format(	
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
    permissions = {"role": "reader", "type": "anyone", "value": None, "withLink": True}	
    file_metadata = {"title": directory_name, "mimeType": G_DRIVE_DIR_MIME_TYPE}	
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
    mime_type = mime_type if mime_type else "text/plain"	
    file_name = file_path.split("/")[-1]	
    return file_name, mime_type	

async def create_token_file(token_file, event):	
    flow = OAuth2WebServerFlow(	
        Var.GDRIVE_CLIENT_ID,	
        Var.GDRIVE_CLIENT_SECRET,	
        OAUTH_SCOPE,	
        redirect_uri=REDIRECT_URI,	
    )	
    authorize_url = flow.step1_get_authorize_url()	
    async with ultroid_bot.conversation(Var.LOG_CHANNEL) as conv:	
        await conv.send_message(	
            f"Go to the following link in your browser: {authorize_url} and reply the code"	
        )	
        response = conv.wait_event(events.NewMessage(chats=Var.LOG_CHANNEL))	
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
    file = drive_service.files().insert(body=body, media_body=media_body)	
    response = None	
    display_message = ""	
    while response is None:	
        status, response = file.next_chunk()	
        await asyncio.sleep(1)	
        if status:	
            percentage = int(status.progress() * 100)	
            progress_str = "[{0}{1}]\nProgress: {2}%\n".format(	
                "".join(["●" for i in range(math.floor(percentage / 5))]),	
                "".join(["" for i in range(20 - math.floor(percentage / 5))]),	
                round(percentage, 2),	
            )	
            current_message = (	
                f"Uploading to G-Drive:\nFile Name: `{file_name}`\n{progress_str}"	
            )	
            if display_message != current_message:	
                try:	
                    await event.edit(current_message)	
                    display_message = current_message	
                except Exception:	
                    pass	
    file_id = response.get("id")	
    drive_service.permissions().insert(fileId=file_id, body=permissions).execute()	
    file = drive_service.files().get(fileId=file_id).execute()	
    download_url = file.get("webContentLink")	
    return download_url

# Gdrive End

def dani_ck(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid


def un_plug(shortname):
    try:
        try:
            for i in LOADED[shortname]:
                ultroid_bot.remove_event_handler(i)
            del LOADED[shortname]
            ADDONS.remove(shortname)

        except BaseException:
            name = f"addons.{shortname}"

            for i in reversed(range(len(ultroid_bot._event_builders))):
                ev, cb = ultroid_bot._event_builders[i]
                if cb.__module__ == name:
                    del ultroid_bot._event_builders[i]
                    del LOADED[shortname]
                    ADDONS.remove(shortname)
    except BaseException:
        raise ValueError


async def dler(sed):
    try:
        await sed.edit("`Fetching data, please wait..`")
    except DownloadError as DE:
        await sed.edit(f"`{str(DE)}`")
    except ContentTooShortError:
        await sed.edit("`The download content was too short.`")
    except GeoRestrictedError:
        await sed.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`",
        )
    except MaxDownloadsReached:
        await sed.edit("`Max-downloads limit has been reached.`")
    except PostProcessingError:
        await sed.edit("`There was an error during post processing.`")
    except UnavailableVideoError:
        await sed.edit("`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        await sed.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        await sed.edit("`There was an error during info extraction.`")
    except Exception as e:
        await sed.edit(f"{str(type(e)): {str(e)}}")


def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def progress(current, total, event, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress_str = "`[{0}{1}] {2}%`\n\n".format(
            "".join(["●" for i in range(math.floor(percentage / 5))]),
            "".join(["" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )
        tmp = (
            progress_str
            + "`{0} of {1}`\n\n`✦ Speed: {2}/s`\n\n`✦ ETA: {3}`\n\n".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                time_formatter(time_to_completion),
            )
        )
        if file_name:
            await event.edit(
                "`✦ {}`\n\n`File Name: {}`\n\n{}".format(type_of_ps, file_name, tmp)
            )
        else:
            await event.edit("`✦ {}`\n\n{}".format(type_of_ps, tmp))


async def restart(ult):
    if Var.HEROKU_APP_NAME and Var.HEROKU_API:
        try:
            Heroku = heroku3.from_key(Var.HEROKU_API)
        except BaseException:
            return await eor(
                ult, "`HEROKU_API` is wrong! Kindly re-check in config vars."
            )
        await eor(ult, "`Restarting your app, please wait for a minute!`")
        app = Heroku.apps()[Var.HEROKU_APP_NAME]
        app.restart()
    else:
        await eor(ult, "`No HEROKU_API_KEY found.\nShutting down. Manually start me.`")
        await ult.client.disconnect()
        os.execl(sys.executable, sys.executable, *sys.argv)


async def get_user_info(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Reply to a user or give a user-id/name.`")
            return None, None
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            return None, None
    return user_obj, extra


def ReTrieveFile(input_file_name):
    RMBG_API = udB.get("RMBG_API")
    headers = {"X-API-Key": RMBG_API}
    files = {"image_file": (input_file_name, open(input_file_name, "rb"))}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r


def ReTrieveURL(input_url):
    RMBG_API = udB.get("RMBG_API")
    headers = {"X-API-Key": RMBG_API}
    data = {"image_url": input_url}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )
    return r


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)
    return image


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await ultroid_bot(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await ultroid_bot(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await ok.edit("`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await ok.edit("`This is a private channel/group or I am banned from there`")
            return None
        except ChannelPublicGroupNaError:
            await ok.edit("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError) as err:
            await ok.edit(str(err))
            return None
    return chat_info


async def fetch_info(chat, event):
    chat_obj_info = await ultroid_bot.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await ultroid_bot(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        print("Exception:", e)
    first_msg_valid = (
        True
        if msg_info and msg_info.messages and msg_info.messages[0].id == 1
        else False
    )
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception as e:
        dc_id = "Unknown"
        str(e)

    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "No"
    )
    slowmode = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "No"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "No"
    )
    verified = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "No"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await ultroid_bot(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            print("Exception:", e)
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b>CHAT INFO:</b>\n"
    caption += f"ID: <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"{chat_type} name: {chat_title}\n"
    if former_title is not None:
        caption += f"Former name: {former_title}\n"
    if username is not None:
        caption += f"{chat_type} type: Public\n"
        caption += f"Link: {username}\n"
    else:
        caption += f"{chat_type} type: Private\n"
    if creator_username is not None:
        caption += f"Creator: {creator_username}\n"
    elif creator_valid:
        caption += (
            f'Creator: <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"Created: <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"Created: <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"Data Centre ID: {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"{chat_type} level: <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"Viewable messages: <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"Messages sent: <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"Messages sent: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"Members: <code>{members}</code>\n"
    if admins is not None:
        caption += f"Administrators: <code>{admins}</code>\n"
    if bots_list:
        caption += f"Bots: <code>{bots}</code>\n"
    if members_online:
        caption += f"Currently online: <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"Restricted users: <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"Banned users: <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'{chat_type} stickers: <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        caption += f"Slow mode: {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
    if not broadcast:
        caption += f"Supergroup: {supergroup}\n\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"Restricted: {restricted}\n"
        if chat_obj_info.restricted:
            caption += f"> Platform: {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> Reason: {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> Text: {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "Scam: <b>Yes</b>\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"Verified by Telegram: {verified}\n\n"
    if description:
        caption += f"Description: \n<code>{description}</code>\n"
    return caption


async def safeinstall(event):
    ok = await eor(event, "`Installing...`")
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await ok.client.download_media(
                await event.get_reply_message(), "addons/"
            )
            xx = open(downloaded_file_name, "r")
            yy = xx.read()
            xx.close()
            try:
                for dan in DANGER:
                    if dan in yy:
                        os.remove(downloaded_file_name)
                        return await eod(
                            ok,
                            "**Installation Aborted**..\n\n`Dangerous plugin.\nMight leak your personal details or can be used to delete you account too`",
                            time=7,
                        )
            except BaseException:
                pass
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_addons(shortname.replace(".py", ""))
                await eod(
                    ok,
                    "✓ `Ultroid - Installed`: `{}` ✓".format(
                        os.path.basename(downloaded_file_name),
                    ),
                    time=3,
                )
            else:
                os.remove(downloaded_file_name)
                await eod(
                    ok, "**ERROR**\nPlugin might have been pre-installed.", time=3
                )
        except Exception as e:
            await eod(ok, "**ERROR\n**" + str(e), time=4)
            os.remove(downloaded_file_name)
    else:
        await eod(
            ok, f"Please use `{Var.HNDLR}install` as reply to a .py file.", time=3
        )


async def allcmds(event):
    x = str(LIST)
    xx = (
        x.replace(",", "\n")
        .replace("[", """\n """)
        .replace("]", "\n\n")
        .replace("':", """ Plugin\n ✘ Commands Available-""")
        .replace("'", "")
        .replace("{", "")
        .replace("}", "")
    )
    t = telegraph.create_page(title="Ultroid All Cmds", content=[f"{xx}"])
    w = t["url"]
    await eod(event, f"All Ultroid Cmds : [Click Here]({w})", link_preview=False)

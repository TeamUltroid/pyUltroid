# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import base64
import os
import random
import string
from logging import WARNING
from random import choice, randrange, shuffle
from traceback import format_exc

from telethon.tl import types
from telethon.utils import get_display_name, get_peer_id

from .. import *
from ..dB import DEVLIST
from ..dB._core import LIST
from ..misc._wrappers import eor
from . import some_random_headers
from .tools import async_searcher, check_filename, json_parser

try:
    import aiofiles
    import aiohttp
except ImportError:
    aiohttp = None
    aiofiles = None

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ManualInputRequired
except ImportError:
    Client = None
    ManualInputRequired = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import cv2
except ImportError:
    cv2 = None
try:
    import numpy as np
except ImportError:
    np = None
try:
    from bs4 import BeautifulSoup
except ImportError:
    LOGS.info("'bs4' not installed.")
    BeautifulSoup = None


async def randomchannel(
    tochat, channel, range1, range2, caption=None, client=ultroid_bot
):
    do = randrange(range1, range2)
    async for x in client.iter_messages(channel, add_offset=do, limit=1):
        caption = caption or x.text
        try:
            await client.send_message(tochat, caption, file=x.media)
        except BaseException:
            pass


# --------------------------------------------------


async def YtDataScraper(url: str):
    to_return = {}
    data = json_parser(
        BeautifulSoup(
            await async_searcher(url),
            "html.parser",
        )
        .find_all("script")[39]
        .text[20:-1]
    )["contents"]
    _common_data = data["twoColumnWatchNextResults"]["results"]["results"]["contents"]
    common_data = _common_data[0]["videoPrimaryInfoRenderer"]
    try:
        description_data = _common_data[1]["videoSecondaryInfoRenderer"]["description"][
            "runs"
        ]
    except (KeyError, IndexError):
        description_data = [{"text": "U hurrr from here"}]
    description = "".join(
        description_datum["text"] for description_datum in description_data
    )

    like_dislike = common_data["videoActions"]["menuRenderer"]["topLevelButtons"]
    to_return["title"] = common_data["title"]["runs"][0]["text"]
    to_return["views"] = (
        common_data["viewCount"]["videoViewCountRenderer"]["shortViewCount"][
            "simpleText"
        ]
        or common_data["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
    )
    to_return["publish_date"] = common_data["dateText"]["simpleText"]
    to_return["likes"] = (
        like_dislike[0]["toggleButtonRenderer"]["defaultText"]["simpleText"]
        or like_dislike[0]["toggleButtonRenderer"]["defaultText"]["accessibility"][
            "accessibilityData"
        ]["label"]
    )
    to_return["dislikes"] = (
        like_dislike[1]["toggleButtonRenderer"]["defaultText"]["simpleText"]
        or like_dislike[1]["toggleButtonRenderer"]["defaultText"]["accessibility"][
            "accessibilityData"
        ]["label"]
    )
    to_return["description"] = description[:250] + "..."
    return to_return


# --------------------------------------------------


async def google_search(query):
    query = query.replace(" ", "+")
    _base = "https://google.com"
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "User-Agent": choice(some_random_headers),
    }
    soup = BeautifulSoup(
        await async_searcher(_base + "/search?q=" + query, headers=headers),
        "html.parser",
    )
    another_soup = soup.find_all("div", class_="ZINbbc xpd O9g5cc uUPGi")
    result = []
    results = [someone.find_all("div", class_="kCrYT") for someone in another_soup]
    for data in results:
        try:
            if len(data) > 1:
                result.append(
                    {
                        "title": data[0].h3.text,
                        "link": _base + data[0].a["href"],
                        "description": data[1].text,
                    }
                )
        except BaseException:
            pass
    return result


# ----------------------------------------------------


async def allcmds(event, telegraph):
    txt = ""
    for z in LIST.keys():
        txt += f"PLUGIN NAME: {z}\n"
        for zz in LIST[z]:
            txt += HNDLR + zz + "\n"
        txt += "\n\n"
    t = telegraph.create_page(title="Ultroid All Cmds", content=[txt])
    await eor(event, f"All Ultroid Cmds : [Click Here]({t['url']})", link_preview=False)


async def ReTrieveFile(input_file_name):
    RMBG_API = udB.get_key("RMBG_API")
    headers = {"X-API-Key": RMBG_API}
    files = {"image_file": open(input_file_name, "rb").read()}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            "https://api.remove.bg/v1.0/removebg", headers=headers, data=files
        ) as out:
            contentType = out.headers.get("content-type")
            if "image" not in contentType:
                return False, (await out.json())

            name = check_filename("ult-rmbg.png")
            file = await aiofiles.open(name, "wb")
            await file.write(await out.read())
            await file.close()
            return True, name


# ---------------- Unsplash Search ----------------
# @New-Dev0


async def unsplashsearch(query, limit=None, shuf=True):
    query = query.replace(" ", "-")
    link = "https://unsplash.com/s/photos/" + query
    extra = await async_searcher(link, re_content=True)
    res = BeautifulSoup(extra, "html.parser", from_encoding="utf-8")
    all_ = res.find_all("img", "YVj9w")
    if shuf:
        shuffle(all_)
    all_ = all_[:limit]
    return [image["src"] for image in all_]


# ---------------- Random User Gen ----------------
# @xditya


async def get_random_user_data():
    base_url = "https://randomuser.me/api/"
    cc = await async_searcher(
        "https://random-data-api.com/api/business_credit_card/random_card", re_json=True
    )
    card = (
        "**CARD_ID:** "
        + str(cc["credit_card_number"])
        + f" {cc['credit_card_expiry_date']}\n"
        + f"**C-ID :** {cc['id']}"
    )
    data_ = (await async_searcher(base_url, re_json=True))["results"][0]
    _g = data_["gender"]
    gender = "🤵🏻‍♂" if _g == "male" else "🤵🏻‍♀"
    name = data_["name"]
    loc = data_["location"]
    dob = data_["dob"]
    msg = """
{} **Name:** {}.{} {}
**Street:** {} {}
**City:** {}
**State:** {}
**Country:** {}
**Postal Code:** {}
**Email:** {}
**Phone:** {}
**Card:** {}
**Birthday:** {}
""".format(
        gender,
        name["title"],
        name["first"],
        name["last"],
        loc["street"]["number"],
        loc["street"]["name"],
        loc["city"],
        loc["state"],
        loc["country"],
        loc["postcode"],
        data_["email"],
        data_["phone"],
        card,
        dob["date"][:10],
    )
    pic = data_["picture"]["large"]
    return msg, pic


# Dictionary (Synonyms and Antonyms)


async def get_synonyms_or_antonyms(word, type_of_words):
    if type_of_words not in ["synonyms", "antonyms"]:
        return "Dude! Please give a corrent type of words you want."
    s = await async_searcher(
        f"https://tuna.thesaurus.com/pageData/{word}", re_json=True
    )
    li_1 = [
        y
        for x in [
            s["data"]["definitionData"]["definitions"][0][type_of_words],
            s["data"]["definitionData"]["definitions"][1][type_of_words],
        ]
        for y in x
    ]
    return [y["term"] for y in li_1]


# --------------------- Instagram Plugin ------------------------- #
# @New-dev0

INSTA_CLIENT = []


async def _insta_login():
    if "insta_creds" in ultroid_bot._cache:
        return ultroid_bot._cache["insta_creds"]
    username = udB.get_key("INSTA_USERNAME")
    password = udB.get_key("INSTA_PASSWORD")
    if username and password:
        settings = eval(udB["INSTA_SET"]) if udB.get_key("INSTA_SET") else {}
        cl = Client(settings)
        try:
            cl.login(username, password)
            ultroid_bot._cache.update({"insta_creds": cl})
        except ManualInputRequired:
            LOGS.exception(format_exc())
            # await get_insta_code(cl, username, password)
            return False
        except LoginRequired:
            udB.del_key("INSTA_SET")
            return await _insta_login()
        except Exception:
            udB.del_key(iter(["INSTA_USERNAME", "INSTA_PASSWORD"]))
            LOGS.exception(format_exc())
            return False
        udB.set_key("INSTA_SET", str(cl.get_settings()))
        cl.logger.setLevel(WARNING)
        return ultroid_bot._cache["insta_creds"]
    return False


async def get_insta_code(username, choice):
    from .. import asst, ultroid_bot

    async with asst.conversation(ultroid_bot.uid, timeout=60 * 2) as conv:
        await conv.send_message(
            "Enter The **Instagram Verification Code** Sent to Your Email.."
        )
        ct = await conv.get_response()
        while not ct.text.isdigit():
            if ct.message == "/cancel":
                await conv.send_message("Cancelled Verification!")
                return
            await conv.send_message(
                "CODE SHOULD BE INTEGER\nSend The Code Back or\nUse /cancel to Cancel Process..."
            )
            ct = await conv.get_response()
        return ct.text


async def create_instagram_client(event):
    if not Client:
        await eor(
            event, "`Instagrapi not Found\nInstall it to use Instagram plugin...`"
        )
        return
    try:
        return INSTA_CLIENT[0]
    except IndexError:
        pass
    from .. import udB

    username = udB.get_key("INSTA_USERNAME")
    password = udB.get_key("INSTA_PASSWORD")
    if not (username and password):
        return
    settings = udB.get_key("INSTA_SET") or {}
    cl = Client(settings)
    cl.challenge_code_handler = get_insta_code
    try:
        cl.login(username, password)
    except ManualInputRequired:
        await eor(event, f"Check Pm From @{asst.me.username}")
        await get_insta_code(cl, username, password)
    except LoginRequired:
        # "login required" refers to relogin...
        udB.del_key("INSTA_SET")
        return await create_instagram_client(event)
    except Exception as er:
        LOGS.exception(er)
        await eor(event, str(er))
        return False
    udB.set_key("INSTA_SET", str(cl.get_settings()))
    cl.logger.setLevel(WARNING)
    INSTA_CLIENT.append(cl)
    return cl


# Quotly


_entities = {
    types.MessageEntityPhone: "phone_number",
    types.MessageEntityMention: "mention",
    types.MessageEntityBold: "bold",
    types.MessageEntityCashtag: "cashtag",
    types.MessageEntityStrike: "strikethrough",
    types.MessageEntityHashtag: "hashtag",
    types.MessageEntityEmail: "email",
    types.MessageEntityMentionName: "text_mention",
    types.MessageEntityUnderline: "underline",
    types.MessageEntityUrl: "url",
    types.MessageEntityTextUrl: "text_link",
    types.MessageEntityBotCommand: "bot_command",
    types.MessageEntityCode: "code",
    types.MessageEntityPre: "pre",
    types.MessageEntitySpoiler: "spoiler",
}


async def _format_quote(event, reply=None, sender=None, type_="private"):
    async def telegraph(file_):
        file = file_ + ".png"
        Image.open(file_).save(file, "PNG")
        files = {"file": open(file, "rb").read()}
        uri = (
            "https://telegra.ph"
            + (
                await async_searcher(
                    "https://telegra.ph/upload", post=True, data=files, re_json=True
                )
            )[0]["src"]
        )
        os.remove(file)
        os.remove(file_)
        return uri

    if reply:
        reply = {
            "name": get_display_name(reply.sender) or "Deleted Account",
            "text": reply.raw_text,
            "chatId": reply.chat_id,
        }
    else:
        reply = {}
    is_fwd = event.fwd_from
    name = None
    last_name = None
    if sender and sender.id not in DEVLIST:
        id_ = get_peer_id(sender)
        name = get_display_name(sender)
    elif not is_fwd:
        id_ = event.sender_id
        sender = await event.get_sender()
        name = get_display_name(sender)
    else:
        id_, sender = None, None
        name = is_fwd.from_name
        if is_fwd.from_id:
            id_ = get_peer_id(is_fwd.from_id)
            try:
                sender = await event.client.get_entity(id_)
                name = get_display_name(sender)
            except ValueError:
                pass
    if sender and hasattr(sender, "last_name"):
        last_name = sender.last_name
    entities = []
    if event.entities:
        for entity in event.entities:
            if type(entity) in _entities:
                enti_ = entity.to_dict()
                del enti_["_"]
                enti_["type"] = _entities[type(entity)]
                entities.append(enti_)
    message = {
        "entities": entities,
        "chatId": id_,
        "avatar": True,
        "from": {
            "id": id_,
            "first_name": (name or (sender.first_name if sender else None))
            or "Deleted Account",
            "last_name": last_name,
            "username": sender.username if sender else None,
            "language_code": "en",
            "title": name,
            "name": name or "Unknown",
            "type": type_,
        },
        "text": event.raw_text,
        "replyMessage": reply,
    }
    if event.document and event.document.thumbs:
        file_ = await event.download_media(thumb=-1)
        uri = await telegraph(file_)
        message["media"] = {"url": uri}

    return message


O_API = "https://bot.lyo.su/quote/generate"


async def create_quotly(
    event,
    url="https://qoute-api-akashpattnaik.koyeb.app/generate",
    reply={},
    bg=None,
    sender=None,
    file_name="quote.webp",
):
    if not isinstance(event, list):
        event = [event]
    from .. import udB

    if udB.get_key("OQAPI"):
        url = O_API
    if not bg:
        bg = "#1b1429"
    content = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": bg,
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": [
            await _format_quote(message, reply=reply, sender=sender)
            for message in event
        ],
    }
    try:
        request = await async_searcher(url, post=True, json=content, re_json=True)
    except ContentTypeError as er:
        if url != O_API:
            return await create_quotly(O_API, post=True, json=content, re_json=True)
        raise er
    if request.get("ok"):
        with open(file_name, "wb") as file:
            image = base64.decodebytes(request["result"]["image"].encode("utf-8"))
            file.write(image)
        return file_name
    raise Exception(str(request))


# Some Sarcasm


def split_list(List, index):
    new_ = []
    while List:
        new_.extend([List[:index]])
        List = List[index:]
    return new_


# https://stackoverflow.com/questions/9041681/opencv-python-rotate-image-by-x-degrees-around-specific-point


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    return cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)


def random_string(length=3):
    """Generate random string of 'n' Length"""
    return "".join(random.choices(string.ascii_uppercase, k=length))


setattr(random, "random_string", random_string)

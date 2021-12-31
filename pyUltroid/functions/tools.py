# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import base64
import json
import math
import os
import random
import re
import ssl
import string
import subprocess
from io import BytesIO
from json.decoder import JSONDecodeError
from traceback import format_exc

import aiohttp
import certifi
import requests
from PIL import Image, ImageDraw, ImageFont
from requests.exceptions import MissingSchema
from telethon import Button

from .. import *
from ..dB.filestore_db import get_stored_msg, store_msg
from .helper import bash

try:
    import cv2
except ImportError:
    cv2 = None
try:
    import numpy as np
except ImportError:
    np = None

try:
    from telegraph import Telegraph
except ImportError:
    Telegraph = None

# ~~~~~~~~~~~~~~~~~~~~OFOX API~~~~~~~~~~~~~~~~~~~~
# @buddhhu


async def get_ofox(codename):
    ofox_baseurl = "https://api.orangefox.download/v3/"
    releases = await async_searcher(
        ofox_baseurl + "releases?codename=" + codename, re_json=True
    )
    device = await async_searcher(
        ofox_baseurl + "devices/get?codename=" + codename, re_json=True
    )
    return device, releases


# ~~~~~~~~~~~~~~~Async Searcher~~~~~~~~~~~~~~~
# @buddhhu


async def async_searcher(
    url: str,
    post: bool = None,
    headers: dict = None,
    params: dict = None,
    json: dict = None,
    data: dict = None,
    ssl=None,
    re_json: bool = False,
    re_content: bool = False,
    real: bool = False,
):
    async with aiohttp.ClientSession(headers=headers) as client:
        if post:
            data = await client.post(url, json=json, data=data, ssl=ssl)
        else:
            data = await client.get(url, params=params, ssl=ssl)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if real:
            return data
        return await data.text()


# ~~~~~~~~~~~~~~~JSON Parser~~~~~~~~~~~~~~~
# @buddhhu


def json_parser(data, indent=None):
    parsed = {}
    try:
        if isinstance(data, str):
            parsed = json.loads(str(data))
            if indent:
                parsed = json.dumps(json.loads(str(data)), indent=indent)
        elif isinstance(data, dict):
            parsed = data
            if indent:
                parsed = json.dumps(data, indent=indent)
    except JSONDecodeError:
        parsed = eval(data)
    return parsed


# ~~~~~~~~~~~~~~~~Link Checker~~~~~~~~~~~~~~~~~


def is_url_ok(url: str):
    try:
        r = requests.head(url)
    except MissingSchema:
        return None
    except BaseException:
        return False
    return r.ok


# ~~~~~~~~~~~~~~~~ Metadata ~~~~~~~~~~~~~~~~~~~~


async def metadata(file):
    out, _ = await bash(f"mediainfo '''{file}''' --Output=JSON")
    data = {}
    try:
        info = json.loads(out)
        info = info["media"]["track"]
        data["title"] = info[0].get("Title") or file.split("/")[-1].split(".")[0]
        data["duration"] = (
            int(float(info[0]["Duration"])) if info[0].get("Duration") else 69
        )
        data["performer"] = (
            info[0].get("Performer")
            or udB.get_key("artist")
            or ultroid_bot.me.first_name
        )
        if len(info) >= 2:
            data["height"] = int(info[1]["Height"]) if info[1].get("Height") else 720
            data["width"] = int(info[1]["Width"]) if info[1].get("Width") else 1280
    except BaseException:
        data["title"] = file.split("/")[-1].split(".")[0]
        data["duration"] = 69
        data["performer"] = udB.get_key("artist") or ultroid_bot.me.first_name
    return data


# ~~~~~~~~~~~~~~~~ Button stuffs ~~~~~~~~~~~~~~~


def get_msg_button(texts: str):
    btn = []
    for z in re.findall("\\[(.*?)\\|(.*?)\\]", texts):
        text, url = z
        urls = url.split("|")
        url = urls[0]
        # if not is_url_ok(url):
        #    continue
        if len(urls) > 1:
            btn[-1].append([text, url])
        else:
            btn.append([[text, url]])

    txt = texts
    for z in re.findall("\\[.+?\\|.+?\\]", texts):
        txt = txt.replace(z, "")

    return txt.strip(), btn


def create_tl_btn(button: list):
    btn = []
    for z in button:
        if len(z) > 1:
            kk = [Button.url(x, y.strip()) for x, y in z]
            btn.append(kk)
        else:
            btn.append([Button.url(z[0][0], z[0][1].strip())])
    return btn


def format_btn(buttons: list):
    txt = ""
    for i in buttons:
        a = 0
        for i in i:
            if hasattr(i.button, "url"):
                a += 1
                if a > 1:
                    txt += f"[{i.button.text} | {i.button.url} | same]"
                else:
                    txt += f"[{i.button.text} | {i.button.url}]"
    _, btn = get_msg_button(txt)
    return btn


# ~~~~~~~~~~~~~~~Saavn Downloader~~~~~~~~~~~~~~~
# @techierror


async def saavn_search(query: str):
    try:
        data = await async_searcher(
            url=f"https://jostapi.herokuapp.com/saavn?query={query.replace(' ', '%20')}",
            re_json=True,
        )
    except BaseException:
        data = None
    return data


# --- webupload ------#
# @buddhhu

_webupload_cache = {}


async def webuploader(chat_id: int, msg_id: int, uploader: str):
    file = _webupload_cache[int(chat_id)][int(msg_id)]
    sites = {
        "anonfiles": {"url": "https://api.anonfiles.com/upload", "json": True},
        "siasky": {"url": "https://siasky.net/skynet/skyfile", "json": True},
        "file.io": {"url": "https://file.io", "json": True},
        "bayfiles": {"url": "https://api.bayfiles.com/upload", "json": True},
        "x0.at": {"url": "https://x0.at/", "json": False},
        "transfer": {"url": "https://transfer.sh", "json": False},
    }
    if uploader and uploader in sites:
        url = sites[uploader]["url"]
        json = sites[uploader]["json"]
    with open(file, "rb") as data:
        # todo: add progress bar
        status = await async_searcher(
            url, data={"file": data.read()}, post=True, re_json=json
        )
    if isinstance(status, dict):
        if "skylink" in status:
            return f"https://siasky.net/{status['skylink']}"
        if status["status"] == 200 or status["status"] is True:
            try:
                link = status["link"]
            except KeyError:
                link = status["data"]["file"]["url"]["short"]
            return link
    del _webupload_cache[int(chat_id)][int(msg_id)]
    return status


def get_all_files(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(os.path.join(root, file))
    return sorted(filelist)


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
                k = len(line) // 55
                for z in range(1, k + 2):
                    lines.append(line[((z - 1) * 55) : (z * 55)])
    return lines[:25]


# ------------------Logo Gen Helpers----------------
# @TechiError


def get_text_size(text, image, font):
    im = Image.new("RGB", (image.width, image.height))
    draw = ImageDraw.Draw(im)
    return draw.textsize(text, font)


def find_font_size(text, font, image, target_width_ratio):
    tested_font_size = 100
    tested_font = ImageFont.truetype(font, tested_font_size)
    observed_width, observed_height = get_text_size(text, image, tested_font)
    estimated_font_size = (
        tested_font_size / (observed_width / image.width) * target_width_ratio
    )
    return round(estimated_font_size)


def make_logo(imgpath, text, funt, **args):
    fill = args.get("fill")
    width_ratio = args.get("width_ratio") or 0.7
    stroke_width = int(args.get("stroke_width"))
    stroke_fill = args.get("stroke_fill")

    img = Image.open(imgpath)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font_size = find_font_size(text, funt, img, width_ratio)
    font = ImageFont.truetype(funt, font_size)
    w, h = draw.textsize(text, font=font)
    draw.text(
        ((width - w) / 2, (height - h) / 2),
        text,
        font=font,
        fill=fill,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )
    file_name = "Logo.png"
    img.save(f"./{file_name}", "PNG")
    img.show()
    return f"{file_name} Generated Successfully!"


# --------------------------------------
# @New-Dev0


async def get_paste(data: str, extension: str = "txt"):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    json = {"content": data, "extension": extension}
    key = await async_searcher(
        url="https://spaceb.in/api/v1/documents/",
        json=json,
        ssl=ssl_context,
        post=True,
        re_json=True,
    )
    try:
        return True, key["payload"]["id"]
    except KeyError:
        if "the length must be between 2 and 400000." in key["error"]:
            return await get_paste(data[-400000:], extension=extension)
        return False, key["error"]
    except Exception as e:
        LOGS.info(e)
        return None, str(e)


# Thanks https://t.me/KukiUpdates/23 for ChatBotApi
async def get_chatbot_reply(message):
    chatbot_base = "https://kukiapi.xyz/api/apikey=ULTROIDUSERBOT/Ultroid/{}/message={}"
    req_link = chatbot_base.format(
        ultroid_bot.me.first_name or "ultroid user",
        message,
    )
    try:
        return (await async_searcher(req_link, re_json=True)).get("reply")
    except Exception:
        LOGS.info(f"**ERROR:**`{format_exc()}`")


def resize_photo(photo):
    """Resize the given photo to 512x512"""
    image = Image.open(photo)
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
        maxsize = (512, 512)
        image.thumbnail(maxsize)
    return image


def check_filename(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid


# ------ Audio \\ Video tools funcn --------#


# https://github.com/1Danish-00/CompressorBot/blob/main/helper/funcn.py#L104


def genss(file):
    process = subprocess.Popen(
        ["mediainfo", file, "--Output=JSON"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = process.communicate()
    out = stdout.decode().strip()
    z = json.loads(out)
    p = z["media"]["track"][0]["Duration"]
    return int(p.split(".")[-2])


def duration_s(file, stime):
    tsec = genss(file)
    x = round(tsec / 5)
    y = round(tsec / 5 + int(stime))
    pin = stdr(x)
    pon = stdr(y) if y < tsec else stdr(tsec)
    return pin, pon


def stdr(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(seconds)) == 1:
        seconds = "0" + str(seconds)
    return (
        ((str(hours) + ":") if hours else "00:")
        + ((str(minutes) + ":") if minutes else "00:")
        + ((str(seconds)) if seconds else "")
    )


# ------------------- used in pdftools --------------------#

# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example


def order_points(pts):
    "get the required points"
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (maxWidth, maxHeight))


# ------------------------------------- Telegraph ---------------------------------- #
TELEGRAPH = []


def telegraph_client():
    if TELEGRAPH:
        return TELEGRAPH[0]

    from .. import udB

    token = udB.get_key("_TELEGRAPH_TOKEN")
    TelegraphClient = Telegraph(token)
    if token:
        TELEGRAPH.append(TelegraphClient)
        return TelegraphClient
    gd_name = ultroid_bot.full_name
    short_name = gd_name[:30]
    profile_url = (
        f"https://t.me/{ultroid_bot.me.username}" if ultroid_bot.me.username else None
    )
    try:
        TelegraphClient.create_account(
            short_name=short_name, author_name=gd_name, author_url=profile_url
        )
    except Exception as er:
        if "SHORT_NAME_TOO_LONG" in str(er):
            TelegraphClient.create_account(
                short_name="ultroiduser", author_name=gd_name, author_url=profile_url
            )
        else:
            LOGS.exception(er)
            return
    udB.set_key("_TELEGRAPH_TOKEN", TelegraphClient.get_access_token())
    TELEGRAPH.append(TelegraphClient)
    return TelegraphClient


async def Carbon(
    code,
    base_url="https://carbonara-42.herokuapp.com/api/cook",
    file_name="ultroid",
    **kwargs,
):
    kwargs["code"] = code
    con = await async_searcher(base_url, post=True, json=kwargs, re_content=True)
    file = BytesIO(con)
    file.name = file_name + ".jpg"
    return file


async def get_file_link(msg):
    from .. import udB

    msg_id = await msg.forward_to(udB.get_key("LOG_CHANNEL"))
    await msg_id.reply(
        "**Message has been stored to generate a shareable link. Do not delete it.**"
    )
    msg_id = msg_id.id
    msg_hash = (
        (
            base64.b64encode(
                "".join(
                    random.choices(string.ascii_letters + string.digits, k=10)
                ).encode("ascii")
            )
        )
        .decode("ascii")
        .replace("=", "")
    )
    store_msg(msg_hash, msg_id)
    return msg_hash


async def get_stored_file(event, hash):
    from .. import udB

    # hash = (base64.b64decode(hash.encode("ascii"))).decode("ascii")
    msg_id = get_stored_msg(hash)
    try:
        msg = await asst.get_messages(udB.get_key("LOG_CHANNEL"), ids=msg_id)
    except Exception as er:
        LOGS.warning(f"FileStore, Error: {er}")
        return
    if msg is None:
        await asst.send_message(
            event.chat_id, "__Message was deleted by owner!__", reply_to=event.id
        )
        return
    await asst.send_message(event.chat_id, msg.text, file=msg.media, reply_to=event.id)


# --------- END --------- #

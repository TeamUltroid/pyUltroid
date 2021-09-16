import io
import json
import math
import os
import ssl
import subprocess
import sys
import traceback

import aiohttp
import certifi
import requests
from PIL import Image, ImageDraw, ImageFont

from . import LOGS, ultroid_bot
from .helper import bash, fast_download, json_parser

try:
    import cv2
except ImportError:
    cv2 = None
try:
    import numpy as np
except ImportError:
    np = None
# ~~~~~~~~~~~~~~~~~~~~OFOX API~~~~~~~~~~~~~~~~~~~~
# @buddhhu


async def get_ofox(codename):
    ofox_baseurl = "https://api.orangefox.download/v3/"
    releases_url = ofox_baseurl + "releases?codename="
    device_url = ofox_baseurl + "devices/get?codename="
    releases = await async_searcher(releases_url + codename)
    device = await async_searcher(device_url + codename)
    return json_parser(device), json_parser(releases)


# ~~~~~~~~~~~~~~~Async Searcher~~~~~~~~~~~~~~~
# @buddhhu


async def async_searcher(url, headers=None, params=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as resp:
            return await resp.text()


# ~~~~~~~~~~~~~~~JSON Parser~~~~~~~~~~~~~~~
# @buddhhu


def json_parser(data, indent=None):
    if isinstance(data, str):
        parsed = json.loads(str(data))
        if indent:
            parsed = json.dumps(json.loads(str(data)), indent=indent)
    elif isinstance(data, dict):
        parsed = data
        if indent:
            parsed = json.dumps(data, indent=indent)
    else:
        parsed = {}
    return parsed


# ~~~~~~~~~~~~~~~Saavn Downloader~~~~~~~~~~~~~~~
# @techierror


async def saavn_dl(query):
    query = query.replace(" ", "%20")
    try:
        data = (
            json_parser(
                await async_searcher(
                    url=f"https://jostapi.herokuapp.com/saavn?query={query}"
                )
            )
        )[0]
    except BaseException:
        return None, None, None, None
    try:
        title = data["song"]
        url = data["media_url"]
        img = data["image"]
        duration = data["duration"]
        performer = data["primary_artists"]
    except BaseException:
        return None, None, None, None
    song = await fast_download(url, filename=title + ".mp3")
    thumb = await fast_download(img, filename=title + ".jpg")
    return song, duration, performer, thumb


# --- webupload ------#
# @buddhhu

CMD_WEB = {
    "anonfiles": 'curl -F "file=@{}" https://api.anonfiles.com/upload',
    "transfer": 'curl --upload-file "{}" https://transfer.sh/',
    "bayfiles": 'curl -F "file=@{}" https://api.bayfiles.com/upload',
    "x0": 'curl -F "file=@{}" https://x0.at/',
    "file.io": 'curl -F "file=@{}" https://file.io',
    "siasky": 'curl -X POST "https://siasky.net/skynet/skyfile" -F "file=@{}"',
}


async def dloader(e, host, file):
    selected = CMD_WEB[host].format(file)
    dn, er = await bash(selected)
    if er:
        text = f"**Error :** `{er}`"
    else:
        text = ""
        keys = json_parser(dn)
        for i in keys.keys():
            text += f"• **{i}** : `{keys[i]}`"
    os.remove(file)
    return await e.edit(text)


# ---------------- Calculator Fucn---------------
# @1danish-00


async def calcc(cmd, event):
    wt = f"print({cmd})"
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexecc(wt, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    if exc:
        return exc
    elif stderr:
        return stderr
    elif stdout:
        return stdout
    return "Success"


async def aexecc(code, event):
    exec("async def __aexecc(event): " + "".join(f"\n {l}" for l in code.split("\n")))

    return await locals()["__aexecc"](event)


# -------------------------------------------------


def get_all_files(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filelist.append(os.path.join(root, file))
    return sorted(filelist)


# ------------------Logo Gen Helpers----------------
# Add ur usernames who created


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


async def get_paste(data, extension="txt"):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    json = {"content": data, "extension": extension}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            "https://spaceb.in/api/v1/documents/", json=json, ssl=ssl_context
        ) as out:
            key = await out.json()
    try:
        return True, key["payload"]["id"]
    except KeyError:
        if "the length must be between 2 and 400000." in key["error"]:
            return await get_paste(data[-400000:], extension=extension)
        return False, key["error"]
    except Exception as e:
        LOGS.info(e)
        return None, str(e)


def get_chatbot_reply(event, message):
    chatbot_base = "https://api.affiliateplus.xyz/api/chatbot?message={message}&botname=Ultroid&ownername={owner}&user=20"
    req_link = chatbot_base.format(
        message=message,
        owner=(ultroid_bot.me.first_name or "ultroid user"),
    )
    try:
        data = requests.get(req_link)
        if data.status_code == 200:
            return (data.json())["message"]
        LOGS.info("**ERROR:**\n`API down, report this to `@UltroidSupport.")
    except Exception as e:
        LOGS.info(f"**ERROR:**`{str(e)}`")


async def resize_photo(photo):
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
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


# --------- END --------- #

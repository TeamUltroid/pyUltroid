import io
import ssl
import sys
import traceback

import aiohttp
import requests
from PIL import Image, ImageDraw, ImageFont

from . import LOGS, ultroid_bot
from .helper import fast_download


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
    width_ratio = args.get("width_ratio") or width_ratio
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

""" Powered by @Google
Available Commands:
.google search <query>
.google image <query>
.google reverse search"""

import asyncio
import aiohttp
import os
import shutil
import time
from bs4 import BeautifulSoup
from datetime import datetime
from telethon.utils import guess_extension
from urllib.parse import urlencode


@borg.on(slitu.admin_cmd(pattern="google search (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    # SHOW_DESCRIPTION = False
    input_str = event.pattern_match.group(1)
    # + " -inurl:(htm|html|php|pls|txt)
    # intitle:index.of \"last modified\"
    # (mkv|mp4|avi|epub|pdf|mp3)"
    input_url = "https://bots.shrimadhavuk.me/search/"
    headers = {"USER-AGENT": "UseTGBot"}
    async with aiohttp.ClientSession() as requests:
        data = {
            "q": input_str,
            "app_id": Config.USE_TG_BOT_APP_ID
        }
        reponse = await requests.get(
            input_url,
            params=data,
            headers=headers
        )
        response = await reponse.json()
    output_str = " "
    for result in response["results"]:
        text = result.get("title")
        url = result.get("url")
        description = result.get("description")
        image = result.get("image")
        output_str += " 👉🏻  [{}]({}) \n\n".format(text, url)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("searched Google for {} in {} seconds. \n{}".format(input_str, ms, output_str), link_preview=False)
    await asyncio.sleep(5)
    await event.edit("Google: {}\n{}".format(input_str, output_str), link_preview=False)


@borg.on(slitu.admin_cmd(pattern="google image (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    work_dir = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY,
        input_str
    )
    if not os.path.isdir(work_dir):
        os.makedirs(work_dir)
    input_url = "https://bots.shrimadhavuk.me/search/"
    headers = {"USER-AGENT": "UseTGBot"}
    url_lst = []
    cap_lst = []
    async with aiohttp.ClientSession() as requests:
        data = {
            "q": input_str,
            "app_id": Config.USE_TG_BOT_APP_ID,
            "p": "GoogleImages"
        }
        reponse = await requests.get(
            input_url,
            params=data,
            headers=headers
        )
        response = await reponse.json()
        for result in response["results"]:
            if len(url_lst) > Config.TG_GLOBAL_ALBUM_LIMIT:
                break
            caption = result.get("description")
            image_url = result.get("url")
            image_req_set = await requests.get(image_url)
            image_file_name = str(time.time()) + "" + guess_extension(
                image_req_set.headers.get("Content-Type")
            )
            image_save_path = os.path.join(
                work_dir,
                image_file_name
            )
            with open(image_save_path, "wb") as f_d:
                f_d.write(await image_req_set.read())
            url_lst.append(image_save_path)
            cap_lst.append(caption)
    if not url_lst:
        await event.edit(f"no results found for {input_str}")
        return
    if len(url_lst) != len(cap_lst):
        await event.edit("search api broken :(")
        return
    await event.reply(
        cap_lst,
        file=url_lst,
        parse_mode="html",
        force_document=True
    )
    for each_file in url_lst:
        os.remove(each_file)
    shutil.rmtree(work_dir, ignore_errors=True)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit(
        f"searched Google for {input_str} in {ms} seconds.",
        link_preview=False
    )
    await asyncio.sleep(5)
    await event.delete()


@borg.on(slitu.admin_cmd(pattern="google reverse search"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    OUTPUT_STR = "Reply to an image to do Google Reverse Search"
    if not event.reply_to_msg_id:
        await event.edit("reply to any media, please -_-")
        return
    await event.edit("Pre Processing Media")
    previous_message = await event.get_reply_message()
    previous_message_text = previous_message.message
    async with aiohttp.ClientSession() as requests:
        BASE_URL = "http://www.google.com"
        if previous_message.media:
            downloaded_file_name = await previous_message.download_media(
                Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": open(downloaded_file_name, "rb"),
                "image_content": ""
            }
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = await requests.post(
                SEARCH_URL,
                data=multipart,
                allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(
                BASE_URL,
                previous_message_text
            )
            google_rs_response = await requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await event.edit("Found Google Result. Pouring some soup on it!")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = await requests.get(the_location, headers=headers)
        soup = BeautifulSoup(
            await response.text(),
            "html.parser"
        )
        # document.getElementsByClassName("r5a77d"): PRS
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = BASE_URL + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        # document.getElementById("jHnbRc")
        img_size_div = soup.find(id="jHnbRc")
        img_size = img_size_div.find_all("div")
        end = datetime.now()
        ms = (end - start).seconds
        out_rts = f"{img_size}\n"
        out_rts += f"<b>Possible Related Search</b>: <a href='{prs_url}'>{prs_text}</a>\n\n"
        out_rts += f"More Info: Open this <a href='{the_location}'>Link</a> in {ms} seconds"
        await event.edit(out_rts, parse_mode="HTML", link_preview=False)


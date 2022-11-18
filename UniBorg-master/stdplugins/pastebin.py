# Copyright (C) 2020 by SpEcHiDe@Github, < https://github.com/SpEcHiDe >.
#
# This file is part of < https://github.com/SpEcHiDe/PyroGramBot > project,
# and is released under the
# "GNU Affero General Public License v3.0 License Agreement".
# Please see < https://github.com/SpEcHiDe/PyroGramBot/raw/master/COPYING >
#

"""IX.IO pastebin like site
Syntax: .paste"""
import os
import aiohttp
from json import loads
from json.decoder import JSONDecodeError
from urllib.parse import urlparse


@borg.on(slitu.admin_cmd(pattern="paste (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    chosen_store = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    ohm = message
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await previous_message.download_media(
                Config.TMP_DOWNLOAD_DIRECTORY
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"

    if message != ohm:
        json_paste_data = {
            "content": message
        }
        # a dictionary to store different pastebin URIs
        paste_bin_store_s = {
            "nekobin": {
                "URL": "https://nekobin.com/api/documents",
                "RAV": "result.key",
                "GAS": "https://github.com/nekobin/nekobin",
            },
            "pasty": {
                "URL": "https://pasty.lus.pm/api/v1/pastes",
                "HEADERS": {
                    "User-Agent": "PyroGramBot/6.9",
                    "Content-Type": "application/json",
                },
                "RAV": "id",
                "GAS": "https://github.com/lus/pasty",
            },
            "pasting": {
                "URL": "https://pasting.codes/api",
            },
            "ixio": {
                "URL": "http://ix.io",
            },
        }
        # get the required pastebin URI
        paste_store_ = paste_bin_store_s.get(
            chosen_store,
            paste_bin_store_s.get("pasty")
        )

        paste_store_url = paste_store_.get("URL")
        paste_store_base_url_rp = urlparse(paste_store_url)

        # the pastebin sites, respond with only the "key"
        # we need to prepend the BASE_URL of the appropriate site
        paste_store_base_url = paste_store_base_url_rp.scheme + \
            "://" + \
            paste_store_base_url_rp.netloc

        async with aiohttp.ClientSession() as session:
            response_d = await session.post(
                paste_store_url,
                json=json_paste_data,
                headers=paste_store_.get("HEADERS")
            )
            response_jn = await response_d.text()
            try:
                response_jn = loads(response_jn.strip())
            except JSONDecodeError:
                # some sites, do not have JSON response
                pass

        rk = paste_store_.get("RAV")
        if rk:
            rkp = rk.split(".")
            for kp in rkp:
                response_jn = response_jn.get(kp)

        else:
            response_jn = response_jn[1:]

        required_url = paste_store_base_url + "/" + response_jn
        await event.edit(required_url, link_preview=False)


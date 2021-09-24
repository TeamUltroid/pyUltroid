# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


import re
from random import choice, randrange, shuffle

import requests
from bs4 import BeautifulSoup as bs
from faker import Faker
from telegraph import Telegraph

from .. import *
from ..dB._core import LIST
from . import some_random_headers
from .tools import async_searcher

# -------------

telegraph = Telegraph()
telegraph.create_account(short_name="Ultroid Cmds List")

# --------------------------------------------------


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


async def quora_scrape(query):
    query = query.replace(" ", "%20")
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "User-Agent": choice(some_random_headers),
    }
    parsed = await async_searcher(
        "https://quora.com/search?q=" + query, headers=headers
    )
    data = re.findall(
        r'window\.ansFrontendGlobals\.data\.inlineQueryResults\.results\[".*?"\] = ("{.*}");',
        x,
    )[-1]
    return json_parser(data)


# --------------------------------------------------


async def google_search(query):
    query = query.replace(" ", "+")
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "User-Agent": choice(some_random_headers),
    }
    soup = bs(
        await async_searcher("https://google.com/search?q=" + query, headers=headers),
        "html.parser",
    )
    another_soup = soup.find_all("div", class_="ZINbbc xpd O9g5cc uUPGi")
    results = []
    result = []
    for someone in another_soup:
        results.append(someone.find_all("div", class_="kCrYT"))
    for data in results:
        try:
            if len(data) > 1:
                result.append(
                    {
                        "title": data[0].h3.text,
                        "link": data[0].a["href"],
                        "description": data[1].text,
                    }
                )
        except BaseException:
            pass
    return result


# ----------------------------------------------------


async def allcmds(event):
    str(LIST)
    txt = ""
    for z in LIST.keys():
        txt += f"PLUGIN NAME: {z}\n"
        for zz in LIST[z]:
            txt += HNDLR + zz + "\n"
        txt += "\n\n"
    t = telegraph.create_page(title="Ultroid All Cmds", content=[f"{xx}"])
    await eor(event, f"All Ultroid Cmds : [Click Here]({t['url']})", link_preview=False)


def ReTrieveFile(input_file_name):
    RMBG_API = udB.get("RMBG_API")
    headers = {"X-API-Key": RMBG_API}
    files = {"image_file": (input_file_name, open(input_file_name, "rb"))}
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


# ---------------- Unsplash Search ----------------
# @New-Dev0


async def unsplashsearch(query, limit=None, shuf=True):
    query = query.replace(" ", "-")
    base_ = "https://unsplash.com"
    link = base_ + "/s/photos/" + query
    extra = await async_searcher(link, re_content=True)
    res = bs(extra, "html.parser", from_encoding="utf-8")
    all = res.find_all("a", "_2Mc8_")
    if shuf:
        shuffle(all)
    all = all[:limit]
    images_src = []
    for img in all:
        ct = await async_searcher(base_ + img["href"], re_content=True)
        bst = bs(ct, "html.parser", from_encoding="utf-8")
        uri = bst.find_all("img", "oCCRx")[0]["src"]
        images_src.append(uri)
    return images_src


# ------------------GoGoAnime Scrapper----------------
# Base Credits - TG@Madepranav


async def airing_eps():
    resp = await async_searcher("https://gogoanime.ai/")
    soup = bs(resp, "html.parser")
    anime = soup.find("nav", {"class": "menu_series cron"}).find("ul")
    air = "**Currently airing anime.**\n\n"
    c = 1
    for link in anime.find_all("a"):
        airing_link = link.get("href")
        name = link.get("title")
        link = airing_link.split("/")
        if c == 21:
            break
        air += f"**{c}.** [{name}]({airing_link})\n"
        c += 1
    return air


async def get_anime_src_res(search_str):
    query = """
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          chapters
          volumes
          season
          type
          format
          status
          duration
          averageScore
          genres
          bannerImage
      }
    }
    """
    tjson = json_parser(
        await async_searcher(
            "https://graphql.anilist.co",
            json={"query": query, "variables": {"search": search_str}},
            post=True,
        ),
    )
    res = list(tjson.keys())
    if "errors" in res:
        return f"**Error** : `{tjson['errors'][0]['message']}`"
    tjson = tjson["data"]["Media"]
    banner = tjson["bannerImage"] if "bannerImage" in tjson.keys() else None
    title = tjson["title"]["romaji"]
    year = tjson["startDate"]["year"]
    episodes = tjson["episodes"]
    link = f"https://anilist.co/anime/{tjson['id']}"
    ltitle = f"[{title}]({link})"
    info = f"**Type**: {tjson['format']}"
    info += "\n**Genres**: "
    for g in tjson["genres"]:
        info += g + " "
    info += f"\n**Status**: {tjson['status']}"
    info += f"\n**Episodes**: {tjson['episodes']}"
    info += f"\n**Year**: {tjson['startDate']['year']}"
    info += f"\n**Score**: {tjson['averageScore']}"
    info += f"\n**Duration**: {tjson['duration']} min\n"
    temp = f"{tjson['description']}"
    info += "__" + (re.sub("<br>", "\n", temp)).strip() + "__"
    return banner, ltitle, year, episodes, info


# ---------------- Random User Gen ----------------
# @xditya


async def get_random_user_data():
    base_url = "https://randomuser.me/api/"
    cc = Faker().credit_card_full().split("\n")
    card = (
        cc[0]
        + "\n"
        + "**CARD_ID:** "
        + cc[2]
        + "\n"
        + f"**{cc[3].split(':')[0]}:**"
        + cc[3].split(":")[1]
    )
    data_ = json_parser(await async_searcher(base_url))["results"][0]
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
    li = [y["term"] for y in li_1]
    return li

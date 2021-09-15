import json

import aiohttp
import requests
from bs4 import BeautifulSoup as bs
from faker import Faker
from telegraph import Telegraph

# -------------

telegraph = Telegraph()
telegraph.create_account(short_name="Ultroid Cmds List")
Client = aiohttp.ClientSession()

# --------------------------------------------------
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
    await eod(event, f"All Ultroid Cmds : [Click Here]({t['url']})", link_preview=False)


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


def unsplashsearch(query, limit=None):
    query = query.replace(" ", "-")
    base_ = "https://unsplash.com"
    link = base_ + "/s/photos/" + query
    async with Client.get(link) as out:
        extra = await out.read()
    res = bs(extra, "html.parser", from_encoding="utf-8")
    all = res.find_all("a", "_2Mc8_")[:count]
    images_src = []
    for img in all:
        async with Client.get(base_ + img["href"]):
            bst = bs(ct, "html.parser", from_encoding="utf-8")
        uri = bst.find_all("img", "oCCRx")[0]["src"]
        images_src.append(uri)
    return images_src


# ------------------GoGoAnime Scrapper----------------
# Base Credits - TG@Madepranav


def airing_eps():
    async with Client.get("https://gogoanime.ai/") as out:
        resp = await out.read()
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


def get_anime_src_res(search_str):
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
    response = (
        requests.post(
            "https://graphql.anilist.co",
            json={"query": query, "variables": {"search": search_str}},
        )
    ).text
    tjson = json.loads(response)
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


def get_random_user_data():
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
    async with Client.get(base_url) as out:
        d = await out.json()
    data_ = d["results"][0]
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

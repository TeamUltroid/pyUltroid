#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  UniBorg Telegram UseRBot
#  Copyright (C) 2021 @UniBorg
#
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
#
# https://github.com/SpEcHiDe/IMDbOT/wiki/Projects-using-this-API

import aiohttp
import json
from telethon.errors import MediaEmptyError


@borg.on(slitu.admin_cmd(pattern="imdb (.*)"))
async def imdb(message):
    try:
        movie_name = message.pattern_match.group(1)
        await message.edit(f"__searching IMDB for__ : `{movie_name}`")
        image_link = None
        if not movie_name.startswith("tt"):
            search_results = await _get(Config.IMDB_API_ONE_URL.format(uniborg=movie_name))
            srch_results = json.loads(search_results)
            first_movie = srch_results.get("d")[0]
            mov_imdb_id = first_movie.get("id")
            image_link = first_movie.get("i").get("imageUrl")
        else:
            mov_imdb_id = movie_name
        mov_link = f"https://www.imdb.com/title/{mov_imdb_id}"
        page2 = await _get(Config.IMDB_API_TWO_URL.format(imdbttid=mov_imdb_id))
        second_page_response = json.loads(page2)
        mov_title = second_page_response.get("title")
        mov_details = get_movie_details(second_page_response)
        director, writer, stars = get_credits_text(second_page_response)
        story_line = second_page_response.get("summary").get("plot", 'Not available')
        mov_country, mov_language = get_countries_and_languages(second_page_response)
        mov_rating = second_page_response.get("UserRating").get("description")
        des_ = f"""<b>Title🎬: </b><code>{mov_title}</code>

<b>More Info: </b><code>{mov_details}</code>
<b>Rating⭐: </b><code>{mov_rating}</code>
<b>Country🗺: </b><code>{mov_country}</code>
<b>Language: </b><code>{mov_language}</code>
<b>Cast Info🎗: </b>
  <b>Director📽: </b><code>{director}</code>
  <b>Writer📄: </b><code>{writer}</code>
  <b>Stars🎭: </b><code>{stars}</code>

<b>IMDB URL Link🔗: </b>{mov_link}

<b>Story Line : </b><em>{story_line}</em>"""
    except IndexError:
        await message.edit("Bruh, Plox enter **Valid movie name** kthx")
        return
    if image_link:
        if len(des_) > 1023:
            des_ = des_[:1023] + "..."
        try:
            await message.respond(
                des_,
                file=image_link,
                parse_mode="html"
            )
        except MediaEmptyError:
            await message.edit(image_link)
            await message.reply(des_, parse_mode="HTML")
        else:
            await message.delete()
    else:
        if len(des_) > 4095:
            des_ = des_[:4095] + "..."
        await message.edit(des_, parse_mode="HTML")


def get_movie_details(soup):
    mov_details = []
    inline = soup.get("Genres")
    if inline and len(inline) > 0:
        for io in inline:
            mov_details.append(io)
    tags = soup.get("duration")
    if tags:
        mov_details.append(tags)
    if mov_details and len(mov_details) > 1:
        mov_details_text = ' | '.join(mov_details)
    else:
        mov_details_text = mov_details[0] if mov_details else ''
    return mov_details_text


def get_countries_and_languages(soup):
    languages = soup.get("Language")
    countries = soup.get("CountryOfOrigin")
    lg_text = ""
    if languages:
        if len(languages) > 1:
            lg_text = ', '.join([lng["NAME"] for lng in languages])
        else:
            lg_text = languages[0]["NAME"]
    else:
        lg_text = "No Languages Found!"
    if countries:
        if len(countries) > 1:
            ct_text = ', '.join([ctn["NAME"] for ctn in countries])
        else:
            ct_text = countries[0]["NAME"]
    else:
        ct_text = "No Country Found!"
    return ct_text, lg_text


def get_credits_text(soup):
    pg = soup.get("sum_mary")
    direc = pg.get("Directors")
    writer = pg.get("Writers")
    actor = pg.get("Stars")
    if direc:
        if len(direc) > 1:
            director = ', '.join([x["NAME"] for x in direc])
        else:
            director = direc[0]["NAME"]
    else:
        director = "No Director Found!"
    if writer:
        if len(writer) > 1:
            writers = ', '.join([x["NAME"] for x in writer])
        else:
            writers = writer[0]["NAME"]
    else:
        writers = "No Writer Found!"
    if actor:
        if len(actor) > 1:
            actors = ', '.join([x["NAME"] for x in actor])
        else:
            actors = actor[0]["NAME"]
    else:
        actors = "No Actor Found!"
    return director, writers, actors


async def _get(url: str, attempts: int = 0):
    if attempts > 5:
        raise IndexError
    async with aiohttp.ClientSession() as requests:
        abc = await requests.get(url)
        cba = await abc.text()
    if abc.status != 200:
        return await _get(url, attempts + 1)
    return cba

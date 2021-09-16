import asyncio
import math
import os
import sys
import time
from traceback import format_exc

import aiofiles
import aiohttp
import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from html_telegraph_poster import TelegraphPoster
from telethon.helpers import _maybe_await

from ..dB._database import Var
from ..dB._core import LOADED, LIST, ADDONS, CMD_HELP
from ..version import ultroid_version
from . import LOGS, eod, eor, ultroid_bot
from .FastTelethon import download_file as downloadable
from .FastTelethon import upload_file as uploadable

UPSTREAM_REPO_URL = Repo().remotes[0].config_reader.get("url").replace(".git", "")


# ----------------- Load \\ Unloader ----------------


def un_plug(shortname):
    try:
        for client in [ultroid_bot, asst]:
            for i in LOADED[shortname]:
                client.remove_event_handler(i)
            try:
                del LOADED[shortname]
                del LIST[shortname]
                ADDONS.remove(shortname)
            except BaseException as er:
                LOGS.info(er)
    except BaseException as er:
        LOGS.info(er)
        name = f"addons.{shortname}"
        for i in reversed(range(len(ultroid_bot._event_builders))):
            ev, cb = ultroid_bot._event_builders[i]
            if cb.__module__ == name:
                del ultroid_bot._event_builders[i]
                try:
                    del LOADED[shortname]
                    del LIST[shortname]
                    ADDONS.remove(shortname)
                except KeyError:
                    pass


async def safeinstall(event):
    ok = await eor(event, "`Installing...`")
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await ok.client.download_media(
                await event.get_reply_message(), "addons/"
            )
            n = event.text
            q = n[9:]
            if q != "f":
                with open(downloaded_file_name, "r") as xx:
                    yy = xx.read()
                try:
                    for dan in DANGER:
                        if re.search(dan, yy):
                            os.remove(downloaded_file_name)
                            return await ok.edit(
                                f"**Installation Aborted.**\n**Reason:** Occurance of `{dan}` in `{downloaded_file_name}`.\n\nIf you trust the provider and/or know what you're doing, use `{HNDLR}install f` to force install.",
                            )
                except BaseException:
                    pass
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_addons(shortname.replace(".py", ""))
                try:
                    plug = shortname.replace(".py", "")
                    if plug in HELP:
                        output = "**Plugin** - `{}`\n".format(plug)
                        for i in HELP[plug]:
                            output += i
                        output += "\n© @TheUltroid"
                        await eod(
                            ok,
                            f"✓ `Ultroid - Installed`: `{plug}` ✓\n\n{output}",
                            time=10,
                        )
                    elif plug in CMD_HELP:
                        kk = f"Plugin Name-{plug}\n\n✘ Commands Available-\n\n"
                        kk += str(CMD_HELP[plug])
                        await eod(
                            ok, f"✓ `Ultroid - Installed`: `{plug}` ✓\n\n{kk}", time=10
                        )
                    else:
                        try:
                            x = f"Plugin Name-{plug}\n\n✘ Commands Available-\n\n"
                            for d in LIST[plug]:
                                x += HNDLR + d
                                x += "\n"
                            await eod(
                                ok, f"✓ `Ultroid - Installed`: `{plug}` ✓\n\n`{x}`"
                            )
                        except BaseException:
                            await eod(
                                ok, f"✓ `Ultroid - Installed`: `{plug}` ✓", time=3
                            )
                except Exception as e:
                    await ok.edit(str(e))
            else:
                os.remove(downloaded_file_name)
                await eod(ok, "**ERROR**\nPlugin might have been pre-installed.")
        except Exception as e:
            await eod(ok, "**ERROR\n**" + str(e))
            os.remove(downloaded_file_name)
    else:
        await eod(ok, f"Please use `{HNDLR}install` as reply to a .py file.")


# ---------------------------------------------


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


# ---------------Updater---------------
# Will add in class


async def updateme_requirements():
    """To Update requirements"""
    reqs = "resources/extras/local-requirements.txt"
    try:
        _, __ = await bash(f"{sys.executable} -m pip install --no-cache-dir -r {reqs}")
    except Exception:
        return format_exc()


def gen_chlog(repo, diff):
    ac_br = repo.active_branch.name
    ch_log = tldr_log = ""
    ch = f"<b>Ultroid {ultroid_version} updates for <a href={UPSTREAM_REPO_URL}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"Ultroid {ultroid_version} updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b><a href={UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater(check_updates=False):
    off_repo = UPSTREAM_REPO_URL
    try:
        repo = Repo()
    except NoSuchPathError as error:
        LOGS.info(f"`directory {error} is not found`")
        Repo().__del__()
        return
    except GitCommandError as error:
        LOGS.info(f"`Early failure! {error}`")
        Repo().__del__()
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)
    ac_br = repo.active_branch.name
    try:
        repo.create_remote("upstream", off_repo)
    except Exception as er:
        LOGS.info(er)
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


# ----------------Fast Upload/Download----------------
# @1danish_00 @new-dev0 @buddhhu


async def uploader(file, name, taime, event, msg):
    with open(file, "rb") as f:
        result = await uploadable(
            client=event.client,
            file=f,
            filename=name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    event,
                    taime,
                    msg,
                ),
            ),
        )
    return result


async def downloader(filename, file, event, taime, msg):
    with open(filename, "wb") as fk:
        result = await downloadable(
            client=event.client,
            location=file,
            out=fk,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    event,
                    taime,
                    msg,
                ),
            ),
        )
    return result


# ~~~~~~~~~~~~~~~~~~~~DDL Downloader~~~~~~~~~~~~~~~~~~~~
# @buddhhu @new-dev0


async def download_file(link, name):
    """for files, without progress callback with aiohttp"""
    async with aiohttp.ClientSession() as ses:
        async with ses.get(link) as re_ses:
            file = await aiofiles.open(name, "wb")
            await file.write(await re_ses.read())
            await file.close()
    return name


async def fast_download(download_url, filename=None, progress_callback=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url, timeout=None) as response:
            if not filename:
                filename = download_url.rpartition("/")[-1]
            total_size = int(response.headers.get("content-length", 0)) or None
            downloaded_size = 0
            with open(filename, "wb") as f:
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                    if progress_callback:
                        await _maybe_await(
                            progress_callback(downloaded_size, total_size)
                        )
            return filename


# ------------------Media Funcns----------------


def make_html_telegraph(title, author, text):
    client = TelegraphPoster(use_api=True)
    client.create_api_token(title)
    page = client.post(
        title=title,
        author=author,
        author_url="https://t.me/TeamUltroid",
        text=text,
    )
    return page["url"]


def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m


# ------------------Some Small Funcs----------------


def time_formatter(milliseconds):
    to_return = ""
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    to_return = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if to_return == "":
        "0 s"
    elif to_return.endswith(":"):
        to_return[:-1]
    else:
        to_return


def humanbytes(size):
    if size in [None, ""]:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            break
        size /= 1024
    return f"{size:.2f} {unit}"


async def progress(current, total, event, start, type_of_ps, file_name=None):
    diff = time.time() - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress_str = "`[{0}{1}] {2}%`\n\n".format(
            "".join("●" for i in range(math.floor(percentage / 5))),
            "".join("" for i in range(20 - math.floor(percentage / 5))),
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


# ------------------System\\Heroku stuff----------------
# @xditya @sppidy @techierror


async def restart(ult):
    if Var.HEROKU_APP_NAME and Var.HEROKU_API:
        try:
            Heroku = heroku3.from_key(Var.HEROKU_API)
            app = Heroku.apps()[Var.HEROKU_APP_NAME]
            await ult.edit("`Restarting your app, please wait for a minute!`")
            app.restart()
        except BaseException:
            return await eor(
                ult,
                "`HEROKU_API` or `HEROKU_APP_NAME` is wrong! Kindly re-check in config vars.",
            )
    else:
        os.execl(sys.executable, sys.executable, "-m", "pyUltroid")


async def shutdown(ult, dynotype="ultroid"):
    ult = await eor(ult, "Shutting Down")
    if Var.HEROKU_APP_NAME and Var.HEROKU_API:
        try:
            Heroku = heroku3.from_key(Var.HEROKU_API)
            app = Heroku.apps()[Var.HEROKU_APP_NAME]
            await ult.edit("`Shutting Down your app, please wait for a minute!`")
            app.process_formation()[dynotype].scale(0)
        except BaseException as e:
            LOGS.info(e)
            return await ult.edit(
                "`HEROKU_API` and `HEROKU_APP_NAME` is wrong! Kindly re-check in config vars."
            )
    else:
        exit(1)


async def heroku_logs(event):
    xx = await eor(event, "`Processing...`")
    if not (Var.HEROKU_API and Var.HEROKU_APP_NAME):
        return await xx.edit("Please set `HEROKU_APP_NAME` and `HEROKU_API` in vars.")
    try:
        app = (heroku3.from_key(Var.HEROKU_API)).app(Var.HEROKU_APP_NAME)
    except BaseException as se:
        LOGS.info(se)
        return await xx.edit(
            "`HEROKU_API` and `HEROKU_APP_NAME` is wrong! Kindly re-check in config vars."
        )
    await xx.edit("`Downloading Logs...`")
    ok = app.get_log()
    with open("ultroid-heroku.log", "w") as log:
        log.write(ok)
    await event.client.send_file(
        event.chat_id,
        file="ultroid-heroku.log",
        thumb="resources/extras/ultroid.jpg",
        caption="**Ultroid Heroku Logs.**",
    )

    os.remove("ultroid-heroku.log")
    await xx.delete()


async def def_logs(ult):
    await ult.client.send_file(
        ult.chat_id,
        file="ultroid.log",
        thumb="resources/extras/ultroid.jpg",
        caption="**Ultroid Logs.**",
    )

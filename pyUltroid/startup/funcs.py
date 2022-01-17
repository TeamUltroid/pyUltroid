# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import asyncio
import logging
import os
import random
import time
from random import randint
from urllib.request import urlretrieve

from pytz import timezone
from telethon.errors import (
    BotMethodInvalidError,
    ChannelPrivateError,
    ChannelsTooMuchError,
    ChatAdminRequiredError,
    UserNotParticipantError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
    JoinChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatPhotoEmpty,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)
from telethon.utils import get_peer_id

from .. import LOGS
from ..configs import Var
from ..functions.helper import download_file, updater

# Better than version_changes?


def update_envs():
    from .. import udB

    for envs in list(os.environ):
        if envs in udB.keys():
            udB.set_key(envs, os.environ[envs])


def startup_stuff():
    from .. import LOGS, udB

    x = ["resources/auth", "resources/downloads", "vcbot/downloads"]
    for x in x:
        if not os.path.isdir(x):
            os.mkdir(x)

    CT = udB.get_key("CUSTOM_THUMBNAIL")
    if CT:
        urlretrieve(CT, "resources/extras/ultroid.jpg")

    GT = udB.get_key("GDRIVE_AUTH_TOKEN")
    if GT:
        with open("resources/auth/gdrive_creds.json", "w") as t_file:
            t_file.write(GT)

    if udB.get_key("AUTH_TOKEN"):
        udB.del_key("AUTH_TOKEN")

    MM = udB.get_key("MEGA_MAIL")
    MP = udB.get_key("MEGA_PASS")
    if MM and MP:
        with open(".megarc", "w") as mega:
            mega.write(f"[Login]\nUsername = {MM}\nPassword = {MP}")

    TZ = udB.get_key("TIMEZONE")
    if TZ:
        try:
            timezone(TZ)
            os.environ["TZ"] = TZ
            time.tzset()
        except AttributeError as er:
            LOGS.exception(er)
        except BaseException:
            LOGS.info(
                "Incorrect Timezone ,\nCheck Available Timezone From Here https://telegra.ph/Ultroid-06-18-2\nSo Time is Default UTC"
            )
            os.environ["TZ"] = "UTC"
            time.tzset()


async def autobot():
    from .. import udB, ultroid_bot

    if udB.get_key("BOT_TOKEN"):
        return
    if Var.BOT_TOKEN:
        return udB.set_key("BOT_TOKEN", Var.BOT_TOKEN)
    await ultroid_bot.start()
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather, Kindly Wait")
    who = ultroid_bot.me
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "ultroid_" + (str(who.id))[5:] + "_bot"
    bf = "@BotFather"
    await ultroid_bot(UnblockRequest(bf))
    await ultroid_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await ultroid_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do.") or "20 bots" in isdone:
        LOGS.info(
            "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
        )
        import sys

        sys.exit(1)
    await ultroid_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await ultroid_bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
            )
            import sys

            sys.exit(1)
    await ultroid_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
    await ultroid_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "ultroid_" + (str(who.id))[6:] + str(ran) + "_bot"
        await ultroid_bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            udB.set_key("BOT_TOKEN", token)
            await ultroid_bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(bf, "Search")
            LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
        else:
            LOGS.info(
                "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
            )

            import sys

            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        udB.set_key("BOT_TOKEN", token)
        await ultroid_bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await ultroid_bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await ultroid_bot.send_message(bf, "Search")
        LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
    else:
        LOGS.info(
            "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )

        import sys

        sys.exit(1)


async def autopilot():
    from .. import asst, udB, ultroid_bot

    if Var.LOG_CHANNEL and str(Var.LOG_CHANNEL).startswith("-100"):
        udB.set_key("LOG_CHANNEL", Var.LOG_CHANNEL)
    channel = udB.get_key("LOG_CHANNEL")
    if channel:
        try:
            chat = await ultroid_bot.get_entity(channel)
        except BaseException:
            logging.exception("message")
            udB.del_key("LOG_CHANNEL")
            channel = None
    if not channel:
        if ultroid_bot._bot:
            LOGS.info("'LOG_CHANNEL' not found! Add it in order to use 'BOTMODE'")
            import sys

            sys.exit()
        LOGS.info("Creating a Log Channel for You!")
        try:
            r = await ultroid_bot(
                CreateChannelRequest(
                    title="My Ultroid Logs",
                    about="My Ultroid Log Group\n\n Join @TeamUltroid",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError:
            LOGS.info(
                "You Are in Too Many Channels & Groups , Leave some And Restart The Bot"
            )
            import sys

            sys.exit(1)
        except BaseException as er:
            LOGS.info(er)
            LOGS.info(
                "Something Went Wrong , Create A Group and set its id on config var LOG_CHANNEL."
            )
            import sys

            sys.exit(1)
        chat = r.chats[0]
        channel = get_peer_id(chat)
        udB.set_key("LOG_CHANNEL", str(channel))
    assistant = True
    try:
        await ultroid_bot.get_permissions(int(channel), asst.me.username)
    except UserNotParticipantError:
        try:
            await ultroid_bot(InviteToChannelRequest(int(channel), [asst.me.username]))
        except BaseException as er:
            LOGS.info("Error while Adding Assistant to Log Channel")
            LOGS.exception(er)
            assistant = False
    except BaseException as er:
        assistant = False
        LOGS.exception(er)
    if assistant:
        try:
            achat = await asst.get_entity(int(channel))
        except BaseException as er:
            achat = None
            LOGS.info("Error while getting Log channel from Assistant")
            LOGS.exception(er)
        if achat and not achat.admin_rights:
            rights = ChatAdminRights(
                add_admins=True,
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                anonymous=False,
                manage_call=True,
            )
            try:
                await ultroid_bot(
                    EditAdminRequest(
                        int(channel), asst.me.username, rights, "Assistant"
                    )
                )
            except ChatAdminRequiredError:
                LOGS.info(
                    "Failed to promote 'Assistant Bot' in 'Log Channel' due to 'Admin Privileges'"
                )
            except BaseException as er:
                LOGS.info("Error while promoting assistant in Log Channel..")
                LOGS.exception(er)
    if isinstance(chat.photo, ChatPhotoEmpty):
        photo = await download_file(
            "https://telegra.ph/file/27c6812becf6f376cbb10.jpg", "channelphoto.jpg"
        )
        ll = await ultroid_bot.upload_file(photo)
        try:
            await ultroid_bot(
                EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll))
            )
        except BaseException as er:
            LOGS.exception(er)
        os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, udB, ultroid_bot

    rem = None
    try:
        chat_id = udB.get_key("LOG_CHANNEL")
        if asst.me.photo:
            return
        LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
        UL = f"@{asst.me.username}"
        if not ultroid_bot.me.username:
            sir = ultroid_bot.me.first_name
        else:
            sir = f"@{ultroid_bot.me.username}"
        file = random.choice(
            [
                "https://telegra.ph/file/92cd6dbd34b0d1d73a0da.jpg",
                "https://telegra.ph/file/a97973ee0425b523cdc28.jpg",
                "resources/extras/ultroid_assistant.jpg",
            ]
        )
        if not os.path.exists(file):
            file = await download_file(file, "profile.jpg")
            rem = True
        msg = await asst.send_message(
            chat_id, "**Auto Customisation** Started on @Botfather"
        )
        await asyncio.sleep(1)
        await ultroid_bot.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await ultroid_bot.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        await ultroid_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await ultroid_bot.send_file("botfather", file)
        await asyncio.sleep(2)
        await ultroid_bot.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await ultroid_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await ultroid_bot.send_message(
            "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
        )
        await asyncio.sleep(2)
        await ultroid_bot.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await ultroid_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await ultroid_bot.send_message(
            "botfather",
            f"✨ PowerFul Ultroid Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @TeamUltroid ✨",
        )
        await asyncio.sleep(2)
        await msg.edit("Completed **Auto Customisation** at @BotFather.")
        if rem:
            os.remove(file)
        LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.exception(e)


async def plug(plugin_channels):
    from .. import ultroid_bot
    from .utils import load_addons

    if ultroid_bot._bot:
        LOGS.info("Plugin Channels can't be used in 'BOTMODE'")
        return
    if not os.path.exists("addons"):
        os.mkdir("addons")
    if not os.path.exists("addons/__init__.py"):
        with open("addons/__init__.py", "w") as f:
            f.write("from plugins import *\n\nbot = ultroid_bot")
    LOGS.info("• Loading Plugins from Plugin Channel(s) •")
    for chat in plugin_channels:
        LOGS.info(f"{'•'*4} {chat}")
        try:
            async for x in ultroid_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument, wait_time=10
            ):
                plugin = x.file.name.replace("_", "-").replace("|", "-")
                if not os.path.exists(f"addons/{plugin}"):
                    await asyncio.sleep(0.6)
                    if x.text == "#IGNORE":
                        continue
                    plugin = await x.download_media(f"addons/{plugin}")
                try:
                    load_addons(plugin.split("/")[-1].replace(".py", ""))
                except Exception as e:
                    LOGS.info(f"Ultroid - PLUGIN_CHANNEL - ERROR - {plugin}")
                    LOGS.exception(e)
                    os.remove(plugin)
        except Exception as er:
            LOGS.exception(er)


# some stuffs


async def ready():
    from .. import asst, udB, ultroid_bot
    from ..functions.helper import inline_mention

    chat_id = udB.get_key("LOG_CHANNEL")
    spam_sent = None
    if not udB.get_key("INIT_DEPLOY"):  # Detailed Message at Initial Deploy
        MSG = """🎇 **Thanks for Deploying Ultroid Userbot!**
• Here, are the Some Basic stuff from, where you can Know, about its Usage."""
        PHOTO = "https://telegra.ph/file/54a917cc9dbb94733ea5f.jpg"
        BTTS = Button.inline("• Click to Start •", "initft_2")
        udB.set_key("INIT_DEPLOY", "Done")
    else:
        MSG = f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: {inline_mention(ultroid_bot.me)}\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @TeamUltroid\n➖➖➖➖➖➖➖➖➖"
        BTTS, PHOTO = None, None
        prev_spam = udB.get_key("LAST_UPDATE_LOG_SPAM")
        if prev_spam:
            try:
                await ultroid_bot.delete_messages(chat_id, int(prev_spam))
            except Exception as E:
                LOGS.info("Error while Deleting Previous Update Message :" + str(E))
        if await updater():
            BTTS = Button.inline("Update Available", "updtavail")

    try:
        spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
    except ValueError as e:
        try:
            await (await ultroid_bot.send_message(chat_id, str(e))).delete()
            spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
        except Exception as g:
            LOGS.info(g)
    except Exception as el:
        LOGS.info(el)
        try:
            spam_sent = await ultroid_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    if spam_sent and not spam_sent.media:
        udB.set_key("LAST_UPDATE_LOG_SPAM", spam_sent.id)
    try:
        # To Let Them know About New Updates and Changes
        await ultroid_bot(JoinChannelRequest("@TheUltroid"))
    except BotMethodInvalidError:
        pass
    except ChannelsTooMuchError:
        LOGS.info("Join @TheUltroid to know about new Updates...")
    except ChannelPrivateError:
        LOGS.info(
            "You are Banned from @TheUltroid for some reason. Contact any dev if you think there is some mistake..."
        )
        import sys

        sys.exit()
    except Exception as er:
        LOGS.exception(er)


async def WasItRestart(udb):
    key = udb.get_key("_RESTART")
    if not key:
        return
    from .. import asst, ultroid_bot

    try:
        data = key.split("_")
        who = asst if data[0] == "bot" else ultroid_bot
        await who.edit_message(
            int(data[1]), int(data[2]), "__Restarted Successfully.__"
        )
    except Exception as er:
        LOGS.exception(er)
    udb.del_key("_RESTART")


def _version_changes(udb):
    for _ in [
        "BOT_USERS",
        "BOT_BLS",
        "VC_SUDOS",
        "SUDOS",
        "CLEANCHAT",
        "LOGUSERS",
        "PLUGIN_CHANNEL",
        "CH_SOURCE",
        "CH_DESTINATION",
        "BROADCAST",
    ]:
        key = udb.get_key(_)
        if key and str(key)[0] != "[":
            key = udb.get(_)
            new_ = [
                int(z) if z.isdigit() or (z.startswith("-") and z[1:].isdigit()) else z
                for z in key.split()
            ]
            udb.set_key(_, new_)

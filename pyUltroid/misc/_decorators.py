# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import asyncio
import inspect
import os
import re
import sys
from pathlib import Path
from time import gmtime, strftime
from traceback import format_exc

from telethon import Button
from telethon import __version__ as telever
from telethon import events
from telethon.errors.rpcerrorlist import (
    AuthKeyDuplicatedError,
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    FloodWaitError,
    MessageDeleteForbiddenError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserIsBotError,
)
from telethon.tl import types
from telethon.utils import get_display_name

from .. import DUAL_HNDLR, HNDLR, LOGS, SUDO_HNDLR, asst, udB, ultroid_bot
from ..dB import DEVLIST
from ..dB._core import LIST, LOADED
from ..dB.sudos import is_fullsudo
from ..functions.helper import bash
from ..functions.helper import time_formatter as tf
from ..version import __version__ as pyver
from ..version import ultroid_version as ult_ver
from . import owner_and_sudos, should_allow_sudo
from ._assistant import admin_check
from ._wrappers import eod

hndlr = "\\" + HNDLR
MANAGER = udB.get("MANAGER")
TAKE_EDITS = udB.get("TAKE_EDITS")
DUAL_MODE = udB.get("DUAL_MODE")
black_list_chats = eval(udB.get("BLACKLIST_CHATS"))


def compile_pattern(data, hndlr):
    if HNDLR == " ":  # No handler feature
        return re.compile("^" + data.replace("^", "").replace(".", ""))
    return (
        re.compile(hndlr + data.replace("^", "").replace(".", ""))
        if data.startswith("^")
        else re.compile(hndlr + data)
    )


# decorator

# Inspiration of ultroid_cmd decor is from RaphielGang/Telegram-Paperlane
# https://github.com/RaphielGang/Telegram-Paperplane/blob/625875a9ecdfd267a53067b3c1580000f5006973/userbot/events.py#L22


def ultroid_cmd(allow_sudo=should_allow_sudo(), **args):
    # With time and addition of Stuff
    # Decorator has turned lengthy and non attractive.
    # Todo : Make it better..
    args["func"] = lambda e: not e.fwd_from and not e.via_bot_id
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args["pattern"]
    black_chats = args.get("chats", None)
    groups_only = args.get("groups_only", False)
    admins_only = args.get("admins_only", False)
    fullsudo = args.get("fullsudo", False)
    allow_all = args.get("allow_all", False)
    type = args.get("type", ["official"])
    only_devs = args.get("only_devs", False)
    allow_pm = args.get("allow_pm", False)
    if isinstance(type, str):
        type = [type]
    if "official" in type and DUAL_MODE:
        type.append("dualmode")

    args["forwards"] = False
    if pattern is not None:
        args["pattern"] = compile_pattern(pattern, hndlr)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except BaseException:
                pass
            try:
                LIST[file_test].append(cmd)
            except BaseException:
                LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    args["blacklist_chats"] = True
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats
    if black_chats is not None:
        if len(black_chats) == 0:
            args["chats"] = []
        else:
            args["chats"] = black_chats

    for i in [
        "admins_only",
        "groups_only",
        "type",
        "allow_all",
        "fullsudo",
        "only_devs",
        "allow_pm",
    ]:
        if i in args:
            del args[i]

    def decorator(func):
        pass

        def doit(mode):
            async def wrapper(ult):
                chat = ult.chat
                if mode in ["dualmode", "official", "sudo"]:
                    if not ult.out and mode in ["dualmode", "sudo"]:
                        if (
                            not allow_all
                            and str(ult.sender_id) not in owner_and_sudos()
                        ):
                            return
                        if fullsudo and not is_fullsudo(ult.sender_id):
                            return await eod(
                                ult, "`Full Sudo User Required...`", time=15
                            )
                    if hasattr(chat, "title"):
                        if (
                            "#noub" in chat.title.lower()
                            and not (chat.admin_rights or chat.creator)
                            and not (ult.sender_id in DEVLIST)
                        ):
                            return
                    if admins_only:
                        if ult.is_private:
                            return await eod(ult, "`Use this in group/channel.`")
                        if not (chat.admin_rights or chat.creator):
                            return await eod(ult, "`I am not an admin.`")
                elif mode == "manager":
                    if not allow_pm and ult.is_private:
                        return
                    else:
                        if not (await admin_check(ult)):
                            return
                else:
                    return
                if only_devs and not udB.get("I_DEV"):
                    return await eod(
                        ult,
                        f"**⚠️ Developer Restricted!**\nIf you know what this does, and want to proceed, use\n`{HNDLR}setredis I_DEV True`.\n\nThis Might Be Dangerous.",
                        time=10,
                    )
                if groups_only and ult.is_private:
                    return await eod(ult, "`Use this in group/channel.`")
                try:
                    await func(ult)
                except FloodWaitError as fwerr:
                    await asst.send_message(
                        int(udB.get("LOG_CHANNEL")),
                        f"`FloodWaitError:\n{str(fwerr)}\n\nSleeping for {tf((fwerr.seconds + 10)*1000)}`",
                    )
                    await asyncio.sleep(fwerr.seconds + 10)
                    await asst.send_message(
                        int(udB.get("LOG_CHANNEL")),
                        "`Bot is working again`",
                    )
                    return
                except ChatSendInlineForbiddenError:
                    return await eod(ult, "`Inline Locked In This Chat.`")
                except (ChatSendMediaForbiddenError, ChatSendStickersForbiddenError):
                    return await eod(
                        ult, "`Sending media or sticker is not allowed in this chat.`"
                    )
                except (BotMethodInvalidError, UserIsBotError) as boterror:
                    return await eod(ult, str(boterror))
                except (
                    MessageIdInvalidError,
                    MessageNotModifiedError,
                    MessageDeleteForbiddenError,
                ):
                    pass
                except AuthKeyDuplicatedError:
                    await asst.send_message(
                        int(udB.get("LOG_CHANNEL")),
                        "Session String expired, create new session from 👇",
                        buttons=[
                            Button.url("Bot", "t.me/SessionGeneratorBot?start="),
                            Button.url(
                                "Repl",
                                "https://replit.com/@TeamUltroid/UltroidStringSession",
                            ),
                        ],
                    )
                    exit()
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except Exception as e:
                    LOGS.exception(e)
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    naam = get_display_name(chat)
                    ftext = "**Ultroid Client Error:** `Forward this to` @UltroidSupport\n\n"
                    ftext += "**Py-Ultroid Version:** `" + str(pyver)
                    ftext += "`\n**Ultroid Version:** `" + str(ult_ver)
                    ftext += "`\n**Telethon Version:** `" + str(telever) + "`\n\n"
                    ftext += "--------START ULTROID CRASH LOG--------"
                    ftext += "\n**Date:** `" + date
                    ftext += "`\n**Group:** `" + str(ult.chat_id) + "` " + str(naam)
                    ftext += "\n**Sender ID:** `" + str(ult.sender_id)
                    ftext += "`\n**Replied:** `" + str(ult.is_reply)
                    ftext += "`\n\n**Event Trigger:**`\n"
                    ftext += str(ult.text)
                    ftext += "`\n\n**Traceback info:**`\n"
                    ftext += str(format_exc())
                    ftext += "`\n\n**Error text:**`\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "`\n\n--------END ULTROID CRASH LOG--------"
                    ftext += "\n\n\n**Last 5 commits:**`\n"

                    stdout, stderr = await bash('git log --pretty=format:"%an: %s" -5')
                    result = str(stdout.strip()) + str(stderr.strip())

                    ftext += result + "`"

                    if len(ftext) > 4096:
                        with open("logs.txt", "w") as log:
                            log.write(ftext)
                        await asst.send_file(
                            int(udB["LOG_CHANNEL"]),
                            "logs.txt",
                            caption="**Ultroid Client Error:** `Forward this to` @UltroidSupport\n\n",
                        )
                        os.remove("logs.txt")
                    else:
                        await asst.send_message(
                            int(udB["LOG_CHANNEL"]),
                            ftext,
                        )

            return wrapper

        if "official" in type:
            args["outgoing"] = True
            ultroid_bot.add_event_handler(doit("official"), events.NewMessage(**args))
            if TAKE_EDITS:
                args["func"] = lambda x: not (
                    isinstance(x.chat, types.Channel) and x.chat.broadcast
                )
                ultroid_bot.add_event_handler(
                    doit("official"),
                    events.MessageEdited(**args),
                )
                args["func"] = lambda e: not e.fwd_from and not e.via_bot_id
            del args["outgoing"]

            if allow_sudo:
                args["outgoing"] = False
                args["pattern"] = compile_pattern(pattern, "\\" + SUDO_HNDLR)
                ultroid_bot.add_event_handler(doit("sudo"), events.NewMessage(**args))
                del args["outgoing"]
        if "assistant" in type:
            args["pattern"] = compile_pattern(pattern, "/")
            asst.add_event_handler(doit("assistant"), events.NewMessage(**args))
        if MANAGER and "manager" in type:
            args["pattern"] = compile_pattern(pattern, "/")
            asst.add_event_handler(doit("manager"), events.NewMessage(**args))

        if "dualmode" in type:
            if not (("manager" in type) and (DUAL_HNDLR == "/")):
                args["pattern"] = compile_pattern(pattern, "\\" + DUAL_HNDLR)
                asst.add_event_handler(doit("dualmode"), events.NewMessage(**args))
        # Collecting all Handlers as one..
        wrapper = doit("official")
        try:
            LOADED[file_test].append(wrapper)
        except Exception:
            LOADED.update({file_test: [wrapper]})

    return decorator

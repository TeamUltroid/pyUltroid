# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from .. import *
from ..utils import *
import re
import inspect
import sys
import asyncio
from telethon import *
from plugins import *
from ..dB.database import Var
from ..dB.core import *
from pathlib import Path
from traceback import format_exc
from time import gmtime, strftime
from asyncio import create_subprocess_shell as asyncsubshell, subprocess as asyncsub
from os import remove
from sys import *

ok = udB.get("SUDOS")
if ok:
    SUDO_USERS = set(int(x) for x in ok.split())
else:
    SUDO_USERS = ""

if SUDO_USERS:
    sudos = list(SUDO_USERS)
else:
    sudos = ""

hndlr = "\\" + Var.HNDLR if Var.HNDLR is not None else "."

# decorator


def ultroid_cmd(allow_sudo=on, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    groups_only = args.get("groups_only", False)
    disable_edited = args.get("disable_edited", True)
    disable_errors = args.get("disable_errors", False)
    trigger_on_fwd = args.get("trigger_on_fwd", False)
    trigger_on_inline = args.get("trigger_on_inline", False)
    args["outgoing"] = True

    if allow_sudo:
        args["from_users"] = sed
        args["incoming"] = True

    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(hndlr + pattern)
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
            except:
                pass
            try:
                LIST[file_test].append(cmd)
            except:
                LIST.update({file_test: [cmd]})
        except:
            pass
    args["blacklist_chats"] = True
    black_list_chats = list(Var.BLACKLIST_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    # check if the plugin should allow edited updates
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        args["allow_edited_updates"]
        del args["allow_edited_updates"]
    if "trigger_on_inline" in args:
        del args["trigger_on_inline"]
    if "disable_edited" in args:
        del args["disable_edited"]
    if "groups_only" in args:
        del args["groups_only"]
    if "disable_errors" in args:
        del args["disable_errors"]
    if "trigger_on_fwd" in args:
        del args["trigger_on_fwd"]
    # check if the plugin should listen for outgoing 'messages'

    def decorator(func):
        async def wrapper(ult):
            if Var.LOG_CHANNEL:
                Var.LOG_CHANNEL
            ult.sender_id
            if not trigger_on_fwd and ult.fwd_from:
                return
            if ult.via_bot_id and not trigger_on_inline:
                return
            if disable_errors:
                return
            if groups_only and not ult.is_group:
                xx = await eor(ult, "`I don't think this is a group.`")
                await asyncio.sleep(5)
                await xx.delete()
                return
            try:
                await func(ult)
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                LOGS.exception(e)
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**Ultroid - Error Report!!**\n"
                    link = "https://t.me/UltroidSupport"
                    text += "If you want you can report it"
                    text += f"- just forward this message [here]({link}).\n"
                    text += "I won't log anything except the fact of error and date\n"

                    ftext = "\nDisclaimer:\nThis file uploaded ONLY here, "
                    ftext += "we logged only fact of error and date, "
                    ftext += "we respect your privacy, "
                    ftext += "you may not report this error if you've "
                    ftext += "any confidential data here, no one will see your data "
                    ftext += "if you choose not to do so.\n\n"
                    ftext += "--------START ULTROID CRASH LOG--------"
                    ftext += "\nDate: " + date
                    ftext += "\nGroup ID: " + str(ult.chat_id)
                    ftext += "\nSender ID: " + str(ult.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(ult.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END ULTROID CRASH LOG--------"

                    command = 'git log --pretty=format:"%an: %s" -5'

                    ftext += "\n\n\nLast 5 commits:\n"

                    process = await asyncsubshell(
                        command, stdout=asyncsub.PIPE, stderr=asyncsub.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

                    ftext += result

                    file = open("ultroid-log.txt", "w+")
                    file.write(ftext)
                    file.close()
                    if Var.LOG_CHANNEL:
                        Placetosend = Var.LOG_CHANNEL
                    else:
                        Placetosend = ultroid_bot.uid
                    await ultroid_bot.asst.send_file(
                        Placetosend,
                        "ultroid-log.txt",
                        caption=text,
                    )
                    remove("ultroid-log.txt")

        if not disable_edited:
            ultroid_bot.add_event_handler(wrapper, events.MessageEdited(**args))
        ultroid_bot.add_event_handler(wrapper, events.NewMessage(**args))
        try:
            LOADED[file_test].append(wrapper)
        except Exception:
            LOADED.update({file_test: [wrapper]})
        return wrapper

    return decorator

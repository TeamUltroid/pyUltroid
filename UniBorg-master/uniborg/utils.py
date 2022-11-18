# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import re
import math
import os
import time
from typing import List, Tuple, Union
from telethon import events
from telethon.utils import add_surrogate
from telethon.tl.custom import Message
from telethon.tl.functions.messages import GetPeerDialogsRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.types import MessageEntityPre, DocumentAttributeFilename
from telethon.tl.types import Channel
from telethon.tl.tlobject import TLObject
from telethon.errors import MessageTooLongError
import datetime

# the secret configuration specific things
from kopp import Config


def admin_cmd(**args):
    args["func"] = lambda e: e.via_bot_id is None

    pattern = args.get("pattern", None)
    allow_sudo = args.get("allow_sudo", False)

    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith("\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(Config.COMMAND_HAND_LER + pattern)

    args["outgoing"] = True
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    args["blacklist_chats"] = True
    black_list_chats = list(Config.UB_BLACK_LIST_CHAT)
    if black_list_chats:
        args["chats"] = black_list_chats

    return events.NewMessage(**args)


async def is_read(borg, entity, message, is_out=None):
    """
    Returns True if the given message (or id) has been read
    if a id is given, is_out needs to be a bool
    """
    is_out = getattr(message, "out", is_out)
    if not isinstance(is_out, bool):
        raise ValueError(
            "Message was id but is_out not provided or not a bool")
    message_id = getattr(message, "id", message)
    if not isinstance(message_id, int):
        raise ValueError("Failed to extract id from message")

    dialog = (await borg(GetPeerDialogsRequest([entity]))).dialogs[0]
    max_id = dialog.read_outbox_max_id if is_out else dialog.read_inbox_max_id
    return message_id <= max_id


async def progress(current, total, event, start, type_of_ps):
    """Generic progress_callback for both
    upload.py and download.py"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        elapsed_time = round(diff)
        if elapsed_time == 0:
            return
        speed = current / diff
        time_to_completion = round((total - current) / speed)
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}]\nPercent: {2}%\n".format(
            ''.join(["█" for _ in range(math.floor(percentage / 5))]),
            ''.join(["░" for _ in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        await event.edit("{}\n {}".format(
            type_of_ps,
            tmp
        ))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {
        0: "",
        1: "Ki",
        2: "Mi",
        3: "Gi",
        4: "Ti"
    }
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(seconds: int) -> str:
    """Inputs time in seconds, to get beautified time,
    as string"""
    result = ""
    v_m = 0
    remainder = seconds
    r_ange_s = {
        "days": (24 * 60 * 60),
        "hours": (60 * 60),
        "minutes": 60,
        "seconds": 1
    }
    for age in r_ange_s:
        divisor = r_ange_s[age]
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m} {age} "
    return result


async def is_admin(client, chat_id, user_id):
    if not str(chat_id).startswith("-100"):
        return False
    try:
        req_jo = await client(GetParticipantRequest(
            channel=chat_id,
            user_id=user_id
        ))
        chat_participant = req_jo.participant
        if isinstance(chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)):
            return True
    except Exception:
        return False
    else:
        return False


# Not that Great but it will fix sudo reply
async def edit_or_reply(event, text):
    if event.sender_id in Config.SUDO_USERS:
        await event.delete()
        reply_to = await event.get_reply_message()
        if reply_to:
            return await reply_to.reply(text)
        else:
            return await event.reply(text)
    else:
        return await event.edit(text)


async def run_command(command: List[str]) -> (str, str):
    process = await asyncio.create_subprocess_exec(
        *command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return t_response, e_response


async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    t_response, e_response = await run_command(file_genertor_command)
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        logger.info(e_response)
        logger.info(t_response)
        return None

# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26

async def cult_small_video(video_file, output_directory, start_time, end_time):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(round(time.time())) + ".mp4"
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name
    ]
    t_response, e_response = await run_command(file_genertor_command)
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        logger.info(e_response)
        logger.info(t_response)
        return None

# these two functions are stolen from
# https://github.com/udf/uniborg/blob/kate/stdplugins/info.py

def parse_pre(text):
    text = text.strip()
    return (
        text,
        [MessageEntityPre(offset=0, length=len(add_surrogate(text)), language='')]
    )


def yaml_format(obj, indent=0, max_str_len=256, max_byte_len=64):
    """
    Pretty formats the given object as a YAML string which is returned.
    (based on TLObject.pretty_format)
    """
    result = []

    if isinstance(obj, TLObject):
        obj = obj.to_dict()

    if isinstance(obj, dict):
        if not obj:
            return 'dict:'
        items = obj.items()
        has_items = len(items) > 1
        has_multiple_items = len(items) > 2
        result.append(obj.get('_', 'dict') + (':' if has_items else ''))
        if has_multiple_items:
            result.append('\n')
            indent += 2
        for k, v in items:
            if k == '_' or v is None:
                continue
            formatted = yaml_format(v, indent)
            if not formatted.strip():
                continue
            result.append(' ' * (indent if has_multiple_items else 1))
            result.append(f'{k}:')
            if not formatted[0].isspace():
                result.append(' ')
            result.append(f'{formatted}')
            result.append('\n')
        if has_items:
            result.pop()
        if has_multiple_items:
            indent -= 2

    elif isinstance(obj, list):
        has_items = len(obj) > 1
        has_multiple_items = len(obj) > 2
        yako = 0
        if has_multiple_items:
            result.append('\n')
            indent += 2
        for one in obj:
            formatted = yaml_format(one, indent)
            if not formatted.strip():
                continue
            result.append(' ' * (indent if has_multiple_items else 1))
            result.append(f'{yako}:')
            if not formatted[0].isspace():
                result.append(' ')
            result.append(f'{formatted}')
            result.append('\n')
            yako += 1
        if has_items:
            result.pop()
        if has_multiple_items:
            indent -= 2

    elif isinstance(obj, str):
        # truncate long strings and display elipsis
        result = repr(obj[:max_str_len])
        if len(obj) > max_str_len:
            result += '…'
        return result

    elif isinstance(obj, bytes):
        # repr() bytes if it's printable, hex like "FF EE BB" otherwise
        if all(0x20 <= c < 0x7f for c in obj):
            return repr(obj)
        else:
            return ('<…>' if len(obj) > max_byte_len else
                    ' '.join(f'{b:02X}' for b in obj))

    elif isinstance(obj, datetime.datetime):
        # ISO-8601 without timezone offset (telethon dates are always UTC)
        return obj.strftime('%Y-%m-%d %H:%M:%S')

    elif hasattr(obj, '__iter__'):
        # display iterables one after another at the base indentation level
        result.append('\n')
        indent += 2
        for x in obj:
            result.append(f"{' ' * indent}- {yaml_format(x, indent + 2)}")
            result.append('\n')
        result.pop()
        indent -= 2
    else:
        return repr(obj)

    return ''.join(result)


async def get_media_lnk(evt_message) -> str:
    if Config.LT_QOAN_NOE_FF_MPEG_URL is None or \
        Config.LT_QOAN_NOE_FF_MPEG_CTD is None:
        return None
    r_m_y = await evt_message.get_reply_message()
    fwd_mesg = await r_m_y.forward_to(
        Config.LT_QOAN_NOE_FF_MPEG_CTD
    )
    return Config.LT_QOAN_NOE_FF_MPEG_URL.format(
        message_id=fwd_mesg.id
    )


async def gmp(message: Message) -> List[Message]:
    if not message.grouped_id:
        return []
    """
    copyied logic from
    https://github.com/pyrogram/pyrogram/blob/ecd83c594cc72e10e13d8c427e817f3495d97252/pyrogram/methods/messages/get_media_group.py#L33"""
    messages = await message.client.get_messages(
        entity=message.chat,
        ids=[
            msg_id for msg_id in range(
                message.id - 9,
                message.id + 10
            )
        ]
    )

    grouped_id = 0
    if len(messages) == 19:
        grouped_id = messages[9].grouped_id
    else:
        grouped_id = messages[message.id-1].grouped_id

    return [
        msg for msg in messages if msg and msg.grouped_id == grouped_id
    ]


def get_message_link(message: Message, fp_: bool) -> str:
    chat_ = message.chat
    if (
        not fp_ and
        hasattr(chat_, "username") and
        chat_.username
    ):
        return (
            f"https://t.me/{chat_.username}/{message.id}"
        )
    chat_id, message_id = None, None
    if isinstance(chat_, Channel):
        chat_id, message_id = chat_.id, message.id
    else:
        chat_id, message_id = "UniBorg", message.id
    return (
        f"https://t.me/c/{chat_id}/{message_id}"
    )


def get_c_m_message(message_link: str) -> Tuple[Union[str, int], int]:
    p_m_link = message_link.split("/")
    chat_id, message_id = None, None
    if len(p_m_link) == 6:
        # private link
        if p_m_link[3] == "c":
            # for supergroups / channels
            chat_id, message_id = int("-100" + p_m_link[4]), int(p_m_link[5])
        elif p_m_link[4] == "UniBorg":
            # for basic groups / private chats
            chat_id, message_id = int(p_m_link[4]), int(p_m_link[5])
    elif len(p_m_link) == 5:
        # public link
        chat_id, message_id = str("@" + p_m_link[3]), int(p_m_link[4])
    return chat_id, message_id

#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  UniBorg Telegram UseRBot
#  Copyright (C) 2021 @UniBorg
#
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you kill yourself" license
#
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!

import asyncio
import os
from datetime import datetime
from telethon.errors import ChannelPrivateError
from time import time


@borg.on(slitu.admin_cmd(pattern="lfcn", allow_sudo=True))
async def _e(evt):
    sm_ = await slitu.edit_or_reply(evt, "...")
    if not evt.reply_to_msg_id:
        await sm_.edit("NO_REPLY_MSG_FOUND")
        return
    reply = await evt.get_reply_message()
    _c, m_ = slitu.get_c_m_message(reply.raw_text)
    try:
        _ok_m_ = await evt.client.get_messages(
            entity=_c,
            ids=m_
        )
    except ChannelPrivateError:
        await sm_.edit("LINK_MARKUP_ID_INVALID")
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    c_time = time()
    start = datetime.now()
    downloaded_file_name = await _ok_m_.download_media(
        Config.TMP_DOWNLOAD_DIRECTORY,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            slitu.progress(d, t, sm_, c_time, "trying to download")
        )
    )
    end = datetime.now()
    ms = (end - start).seconds
    await sm_.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))

# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .startup.BaseClient import UltroidClient
from .startup.connections import RedisConnection, session_file
from .dB._database import Var
udB = RedisConnection(host="", port=None, password="", platform=where_hosted())

ultroid_bot = UltroidClient(
    session_file(), api_id=Var.API_ID, api_hash=Var.API_HASH, plugins_path="plugins"
)
asst = UltroidClient(None, api_id=None, api_hash="", bot_token=Var.BOT_TOKEN)

# Some Automations

ultroid_bot.run()

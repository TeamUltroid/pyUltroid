# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


from .startup.connections import RedisConnection
from .startup.BaseClient import UltroidClient

udB = RedisConnection(host="", port=None, password="", platform=where_hosted())

ultroid_bot = UltroidClient(get_session(), api_id=None, api_hash="", plugins_path="plugins")
asst = UltroidClient("Needed?", api_id=None, api_hash="", bot_token="")

# Some Automations

ultroid_bot.run()

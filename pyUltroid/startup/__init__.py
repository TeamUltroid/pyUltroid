# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import time
from logging import INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger

from safety.tools import *
from telethon import __version__

from ..version import __version__ as __pyUltroid__
from ..version import ultroid_version

if os.path.exists("ultroid.log"):
    os.remove("ultroid.log")

LOGS = getLogger("pyUltLogs")
TeleLogger = getLogger("Telethon")
TeleLogger.setLevel(WARNING)

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler("ultroid.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)


LOGS.info(f"py-Ultroid Version - {__pyUltroid__}")
LOGS.info(f"Telethon Version - {__version__}")
LOGS.info(f"Ultroid Version - {ultroid_version}")

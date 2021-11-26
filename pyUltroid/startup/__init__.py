# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import sys
import time
from logging import (
    DEBUG,
    INFO,
    WARNING,
    FileHandler,
    StreamHandler,
    basicConfig,
    getLogger,
)

from safety.tools import *
from telethon import __version__

from ..version import __version__ as __pyUltroid__
from ..version import ultroid_version

file = "ultroid.log"
if len(sys.argv) > 6:
    file = f"ultroid{sys.argv[6]}.log"

if os.path.exists(file):
    os.remove(file)

LOGS = getLogger("pyUltLogs")
TelethonLogger = getLogger("Telethon")
TelethonLogger.setLevel(DEBUG)

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    level=DEGUG,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler(file), StreamHandler()],
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

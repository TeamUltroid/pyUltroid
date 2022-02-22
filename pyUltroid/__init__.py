# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import sys

run_as_module = False

if sys.argv[0].endswith("pyUltroid/__main__.py"):
    run_as_module = True
    from .init import *

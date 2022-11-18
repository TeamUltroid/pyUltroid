


import asyncio
import importlib
import glob
import sys
import os
from pathlib import Path

from config import Config
from Alexa import bot, tbot, H2, H3, H4, H5
from Alexa.utils import (join_it, load_module, 
                                logger_check, plug_channel, 
                                start_msg, update_sudo)
# from telegram.session import __version__
HELL_PIC = "https://telegra.ph/file/ae8d0b4f61ae5d4121671.png"


async def Alexa(session=None, client=None, session_name="Main"):
    if session:
        logger_check.info(f"••• Starting Client [{session_name}] •••")
        try:
            await client.start()
            return 1
        except:
            logger_check.error(f"Error in {session_name}!! Check & try again!")
            return 0
    else:
        return 0

# Load plugins based on config UNLOAD
async def plug_load(path):
    files = glob.glob(path)
    for name in files:
        with open(name) as hell:
            path1 = Path(hell.name)
            shortname = path1.stem
            if shortname.replace(".py", "") in Config.UNLOAD:
                os.remove(Path(f"TelethonHell/plugins/{shortname}.py"))
            else:
                load_module(shortname.replace(".py", ""))
                
# Final checks after startup
async def hell_is_on(total):
    await update_sudo()
    await logger_check(bot)
    await start_msg(tbot, HELL_PIC, "", total)
    await join_it(bot)
    await join_it(H2)
    await join_it(H3)
    await join_it(H4)
    await join_it(H5)


# Hellbot starter...
async def start_bot():
    try:
        tbot_id = await tbot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"
        bot.tgbot = tbot
        logger_check.info("••• Starting (TELETHON) •••")
        C1 = await Alexa(Config.STRING_SESSION, bot, "STRING_SESSION")
        C2 = await Alexa(Config.SESSION_2, H2, "SESSION_2")
        C3 = await Alexa(Config.SESSION_3, H3, "SESSION_3")
        C4 = await Alexa(Config.SESSION_4, H4, "SESSION_4")
        C5 = await Alexa(Config.SESSION_5, H5, "SESSION_5")
        await tbot.start()
        total = C1 + C2 + C3 + C4 + C5
        logger_check.info("••• Startup Completed •••")
        logger_check.info("••• Starting to load Plugins •••")
        await plug_load("Alexa/plugins/*.py")
        await plug_channel(bot, Config.PLUGIN_CHANNEL)
        logger_check.info("⚡ Alexa Is Now Working ⚡")
        logger_check.info("This is for personal checking purposes only. you can report the bugs but you cant blame me if you getting bad output")
        logger_check.info(f"» Total Clients = {str(total)} «")
        await hell_is_on(total)
    except Exception as e:
        logger_check.error(f"{str(e)}")
        sys.exit()


bot.loop.run_until_complete(start_bot())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    try:
        bot.run_until_disconnected()
    except ConnectionError:
        pass


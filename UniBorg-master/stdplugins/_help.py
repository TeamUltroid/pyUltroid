"""**Know Your UniBorg**
◇ list of all loaded plugins
◆ `.helpme`\n
◇ to know Data Center
◆ `.dc`\n
◇ powered by
◆ `.config`\n
◇ to know syntax
◆ `.syntax` <plugin name>
"""

import shutil
import sys
import time
from telethon import events, functions, __version__


@borg.on(slitu.admin_cmd(pattern="helpme ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    splugin_name = event.pattern_match.group(1)
    if splugin_name in borg._plugins:
        s_help_string = borg._plugins[splugin_name].__doc__
    else:
        s_help_string = ""
    _, check_sgnirts = check_data_base_heal_th()

    current_run_time = slitu.time_formatter((time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage("/")
    total = slitu.humanbytes(total)
    used = slitu.humanbytes(used)
    free = slitu.humanbytes(free)

    help_string = "@UniBorg\n"
    help_string += f"✅ <b>UpTime</b> <code>{current_run_time}</code>\n"
    help_string += f"✅ <b>Python</b> <code>{sys.version}</code>\n"
    help_string += f"✅ <b>Telethon</b> <code>{__version__}</code>\n"
    help_string += f"{check_sgnirts} <b>Database</b>\n"
    help_string += f"<b>Total Disk Space</b>: <code>{total}</code>\n"
    help_string += f"<b>Used Disk Space</b>: <code>{used}</code>\n"
    help_string += f"<b>Free Disk Space</b>: <code>{free}</code>\n\n"
    help_string += f"UserBot Forked from https://github.com/udf/uniborg"
    borg._iiqsixfourstore[str(event.chat_id)] = {}
    borg._iiqsixfourstore[
        str(event.chat_id)
    ][
        str(event.id)
    ] = help_string + "\n\n" + s_help_string
    if borg.tgbot:
        tgbot_username = await tgbot.get_me()
        results = await borg.inline_query(  # pylint:disable=E0602
            tgbot_username,
            f"@UniBorg {event.chat_id} {event.id}"
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
    else:
        await event.reply(
            help_string + "\n\n" + s_help_string,
            parse_mode="html"
        )

    await event.delete()


@borg.on(slitu.admin_cmd(pattern="dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(result.stringify())


@borg.on(slitu.admin_cmd(pattern="config"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetConfigRequest())  # pylint:disable=E0602
    result = result.stringify()
    logger.info(result)  # pylint:disable=E0602
    await event.edit("""Telethon UserBot powered by @UniBorg""")


@borg.on(slitu.admin_cmd(pattern="syntax (.*)"))
async def _(event):
    if event.fwd_from:
        return
    plugin_name = event.pattern_match.group(1)
    if plugin_name in borg._plugins:
        help_string = borg._plugins[plugin_name].__doc__
        unload_string = f"Use `.unload {plugin_name}` to remove this plugin.\n           © @UniBorg"
        if help_string:
            plugin_syntax = f"Syntax for plugin **{plugin_name}**:\n\n{help_string}\n{unload_string}"
        else:
            plugin_syntax = f"No DOCSTRING has been setup for {plugin_name} plugin."
    else:
        plugin_syntax = "Enter valid **Plugin** name.\nDo `.exec ls stdplugins` or `.helpme` to get list of valid plugin names."
    await event.edit(plugin_syntax)


""" h
t
t UniBorg Telegram UseRBot 
p Copyright (C) 2020 @UniBorg
s
: This code is licensed under
/
/
g the "you can't use this for anything - public or private,
i unless you know the two prime factors to the number below" license
t
. 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
to
g വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ
r ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
and
.
xyz
/
uniborg
/
uniborg"""
def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "❌"

    if not Config.DB_URI:
        return is_database_working, output

    from sql_helpers import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "✅"
        is_database_working = True

    return is_database_working, output

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
from math import ceil
import asyncio
import json
import re
from telethon import events, custom


@borg.on(slitu.admin_cmd(  # pylint:disable=E0602
    pattern="ib (.[^ ]*) (.*)"
))
async def _(event):
    # https://stackoverflow.com/a/35524254/4723940
    if event.fwd_from:
        return
    bot_username = event.pattern_match.group(1)
    search_query = event.pattern_match.group(2)
    try:
        output_message = ""
        bot_results = await event.client.inline_query(
            bot_username,
            search_query
        )
        for i, result in enumerate(bot_results):
            output_message += "{} {} `{}`\n\n".format(
                result.title,
                result.description,
                ".icb " + bot_username + " " + str(i + 1) + " " + search_query
            )
        await event.edit(output_message)
    except Exception as e:
        await event.edit("{} did not respond correctly, for **{}**!\n\
            `{}`".format(bot_username, search_query, str(e)))


@borg.on(slitu.admin_cmd(  # pylint:disable=E0602
    pattern="icb (.[^ ]*) (.[^ ]*) (.*)"
))
async def _(event):
    if event.fwd_from:
        return
    bot_username = event.pattern_match.group(1)
    i_plus_oneth_result = event.pattern_match.group(2)
    search_query = event.pattern_match.group(3)
    try:
        bot_results = await event.client.inline_query(
            bot_username,
            search_query
        )
        message = await bot_results[int(i_plus_oneth_result) - 1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
        await event.delete()
    except Exception as e:
        await event.edit(str(e))


# pylint:disable=E0602
if Config.TG_BOT_USER_NAME_BF_HER is not None and borg.tgbot is not None:
    @borg.tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.sender_id == borg.uid and query.startswith("@UniBorg "):
            try:
                _, ko, pno = query.split(" ")
                actual_text = borg._iiqsixfourstore[ko][pno]
                del borg._iiqsixfourstore[ko]
            except IndexError:
                actual_text = query
            buttons = paginate_help(0, borg._plugins, "helpme")
            result = builder.article(
                "© @UniBorg",
                text="{}\nCurrently Loaded Plugins: {}".format(
                    actual_text, len(borg._plugins)
                ),
                buttons=buttons,
                link_preview=False,
                parse_mode="html"
            )
        elif query.startswith("tb_btn"):
            result = builder.article(
                "Button Parser © @UniBorg",
                text=f"powered by @UniBorg",
                buttons=[],
                link_preview=True,
                parse_mode="html"
            )
        else:
            result = builder.article(
                "© @UniBorg",
                text=(
                    "Try @UniBorg\n"
                    "You can log-in as Bot or User and do many cool things with your Telegram account.\n\n"
                    "All instructions to run @UniBorg in your PC has been explained in https://github.com/SpEcHiDe/UniBorg"
                ),
                buttons=[
                    [custom.Button.url("Join the Channel", "https://telegram.dog/UniBorg"), custom.Button.url(
                        "Join the Group", "tg://some_unsupported_feature")],
                    [custom.Button.url(
                        "Source Code", "tg://some_unsupported_feature")]
                ],
                link_preview=False,
                parse_mode="html"
            )
        await event.answer([result] if result else None)

    @borg.tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"helpme_next\((.+?)\)")
    ))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == borg.uid:  # pylint:disable=E0602
            current_page_number = int(
                event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number + 1, borg._plugins, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own @UniBorg, and don't edit my messages!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @borg.tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"helpme_prev\((.+?)\)")
    ))
    async def on_plug_in_callback_query_handler(event):
        if event.sender_id == borg.uid:  # pylint:disable=E0602
            current_page_number = int(
                event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1,
                borg._plugins,  # pylint:disable=E0602
                "helpme"
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own @UniBorg, and don't edit my messages!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @borg.tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"ub_plugin_(.*)")
    ))
    async def on_plug_in_callback_query_handler(event):
        plugin_name = event.data_match.group(1).decode("UTF-8")
        try:
            help_string = borg._plugins[plugin_name].__doc__[
                0:125
            ]  # pylint:disable=E0602
        except (ValueError, TypeError):
            help_string = None
        reply_pop_up_alert = help_string if help_string is not None else \
            "No DOCSTRING has been setup for {} plugin".format(plugin_name)
        reply_pop_up_alert += "\n\n Use .unload {} to remove this plugin\n\
            © @UniBorg".format(plugin_name)
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = Config.NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD
    number_of_cols = 2
    helpable_plugins = [p for p in loaded_plugins if not p.startswith("_")]
    helpable_plugins = sorted(helpable_plugins)
    modules = [custom.Button.inline(
        "{} {}".format("✅", x),
        data="ub_plugin_{}".format(x))
        for x in helpable_plugins]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[modulo_page * number_of_rows:number_of_rows * (modulo_page + 1)] + \
            [
            (custom.Button.inline("Previous", data="{}_prev({})".format(prefix, modulo_page)),
             custom.Button.inline("Next", data="{}_next({})".format(prefix, modulo_page)))
        ]
    return pairs

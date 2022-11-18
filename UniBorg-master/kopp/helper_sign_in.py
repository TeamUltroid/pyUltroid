#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  UniBorg Telegram UseRBot
#  Copyright (C) 2020 @UniBorg
# (c) https://t.me/TelethonChat/37677
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
#
# 76420267623546914285312953847595971404341698667641514250876752277272387319730719447944190236554292723287731288464885804750741761364327420735484520254795074034271100312534358762695139153809201139028342591690162180482749102700757709533577692364027644748874488672927686880394116645482754406114234995849466230628072343395577643542244898329670772406248890522958479425726186109846556166785296629623349390742033833661187669196367578138285625089404848643493377827537273669265993240595087539269421233264244215402846901329418276845584435165797641413600630197168449069124329071377882018664252635437935498247362577995000876370559921979986167467150242719108997966389358573614338347798942075025019524334410765076448079346402255279475454578911100171143362383701997345247071665044229776967047890105530288552675523382282543070978365198408375296102481704475022808512560332288875562645323407287276387630426464690604583020202716621432448074540765228575710411577376747565205168211778277438102839283208230298551765603915629876539090653002258100860161813070337131517342747019595180737118037884721995383231810660641212174692945512923696997890453647367133871298033535417493414711299792390309624922324695948156041420140711933411174201608157710806470205328887
#
# https://github.com/udf/uniborg/raw/kate/stdplugins/sp_lonami_gay.py
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!

import logging
import secrets
from telethon import TelegramClient
from alchemysession import AlchemySessionContainer
from telethon.errors.rpcerrorlist import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError
)


async def bleck_megick(event, config_jbo, session_id):
    if not event.is_private:
        return
    bot_me = await event.client.get_me()
    logging.info(bot_me.stringify())
    # force int for Type checks
    # validations
    async with event.client.conversation(event.chat_id) as conv:
        await conv.send_message(
            "welcome **master**\n"
            "please send me your Phone Number, to generate "
            "`HU_STRING_SESSION` \n"
            "Enter the Phone Number that you want to make awesome, "
            "powered by @UniBorg"
        )

        msg2 = await conv.get_response()
        logging.info(msg2.stringify())
        phone = msg2.message.strip()
        container = AlchemySessionContainer(config_jbo.DB_URI)
        if not session_id:
            session_id = str(secrets.randbelow(1000000))
        reel_sess_id = session_id.split(" ")[0]
        session = container.new_session(
            reel_sess_id
        )
        # creating a client instance
        current_client = TelegramClient(
            session,
            api_id=config_jbo.APP_ID,
            api_hash=config_jbo.API_HASH,
            device_model="GNU/Linux nonUI",
            app_version="@UniBorg 3.0",
            lang_code="ml",
        )
        if config_jbo.SROSTERVECK in session_id:
            # o14mF
            current_client.session.set_dc(
                int(session_id.split(" ")[1]),
                session_id.split(" ")[2],
                int(session_id.split(" ")[3])
            )
        # init: connection to tg servers
        await current_client.connect()
        # send a code request
        sent = await current_client.send_code_request(phone)
        logging.info(sent)
        if not sent:
            await conv.send_message(
                "This number is not registered on Telegram. "
                "Please check your #karma by reading https://t.me/c/1220993104/28753"
            )
            return

        await conv.send_message(
            "This number is registered on Telegram. "
            "Please input the verification code "
            "that you receive from [Telegram](tg://user?id=777000) "
            "seperated by space, "
            "else a `PhoneCodeInvalidError` would be raised."
        )
        msg4 = await conv.get_response()

        received_code = msg4.message.strip()
        received_tfa_code = None
        received_code = "".join(received_code.split(" "))

        try:
            await current_client.sign_in(
                phone,
                code=received_code,
                password=received_tfa_code
            )
        except PhoneCodeInvalidError:
            await conv.send_message(
                "Invalid Code Received. "
                "Please re /start"
            )
            return
        except SessionPasswordNeededError:
            await conv.send_message(
                "The entered Telegram Number is protected with 2FA. "
                "Please enter your second factor authentication code.\n"
                "__This message "
                "will only be used for generating your string session, "
                "and will never be used for any other purposes "
                "than for which it is asked.__"
                "\n\n"
                "The code is available for review at @UniBorg"
            )
            msg6 = await conv.get_response()
            received_tfa_code = msg6.message.strip()
            await current_client.sign_in(password=received_tfa_code)

        # all done
        # Getting information about yourself
        current_client_me = await current_client.get_me()
        # "me" is an User object. You can pretty-print
        # any Telegram object with the "stringify" method:
        logging.info(current_client_me.stringify())

        string_session_messeg = await conv.send_message(
            f"{reel_sess_id}"
        )
        await string_session_messeg.reply(
            "now, "
            "please turn of the application "
            "and set the above variable to "
            "`HU_STRING_SESSION` variable, "
            "and restart application."
        )

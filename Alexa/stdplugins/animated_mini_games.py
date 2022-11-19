"""@RollADie and @AnimatedDart
Viewer and Executor discretion is advised,
while executing / running any parts of the code
Nobody is reponsible for your account,
Your account might get banned for offensive use of this script,
The below script is only intended for "fun" and "entertainment"
and please read https://t.me/UniBorg/39 before proceeding to run this!"""
from telethon.tl.types import InputMediaDice

# EMOJI CONSTANTS
DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
FOOT_E_MOJI = "⚽"
SLOT_M_MOJI = "🎰"
BAII_E_MOJI = "🎳"
# EMOJI CONSTANTS

#TODO: get emojies from AppConfig ? :\\



@borg.on(slitu.admin_cmd(
    pattern=f"({DART_E_MOJI}|{DICE_E_MOJI}|{BALL_E_MOJI}|{FOOT_E_MOJI}|{SLOT_M_MOJI}|{BAII_E_MOJI}) ?(.*)")
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except:
            pass

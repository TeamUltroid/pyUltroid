"""This Module was inspired by
@TwitFace 's https://t.me/c/1356929597/86989"""

from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.help import GetAppConfigRequest
from telethon.tl.types import InputStickerSetDice


@borg.on(slitu.admin_cmd(pattern="watmg", allow_sudo=True))
async def _(event):
    status_message = await slitu.edit_or_reply(event, "...")
    config = await event.client(GetAppConfigRequest())
    emojies = next(
        (x for x in config.value if x.key == "emojies_send_dice")
    )
    ystes = {}
    for emoji in emojies.value.value:
        sticker_set = await event.client(
            GetStickerSetRequest(
                InputStickerSetDice(
                    emoji.value
                )
            )
        )
        ystes[emoji.value] = f"https://t.me/addstickers/{sticker_set.set.short_name}"
    oprtts = ""
    for yek in ystes:
        oprtts += f"{yek} {ystes.get(yek)}\n"
    await status_message.edit(oprtts, parse_mode="html")

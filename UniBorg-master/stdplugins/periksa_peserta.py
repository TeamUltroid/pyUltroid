"""#Telegram #Failures

#768

by @UniBorg"""

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError


@borg.on(slitu.admin_cmd(pattern="pep ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    s_ = await event.reply(".")
    input_str = event.pattern_match.group(1)
    chat = event.chat_id
    reply = await event.get_reply_message()
    await event.delete()
    if not input_str and reply:
        input_str = reply.sender_id
    else:
        input_str = input_str.strip()
        if input_str.isnumeric():
            input_str = int(input_str)
    try:
        rpoi = await event.client(GetParticipantRequest(
            channel=chat,
            user_id=input_str
        ))
    except UserNotParticipantError:
        await s_.edit(f"user `{input_str}` has not joined `{chat}`")
    else:
        participant = rpoi.participant
        new_ko = {}
        available_kinds = (
            "user_id",
            "promoted_by",
            "kicked_by"
        )
        for kind in available_kinds:
            poid = getattr(participant, kind, None)
            if poid is not None:
                epoid = await event.client.get_entity(poid)
                new_ko[kind] = epoid
        await s_.edit(f"`{borg.secure_text(slitu.yaml_format(new_ko))}`")


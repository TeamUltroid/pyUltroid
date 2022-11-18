"""Check your internet speed powered by speedtest.net
Syntax: .speedtest
Available Options: image, file, text"""
from datetime import datetime
import io
import speedtest


@borg.on(slitu.admin_cmd(pattern="speedtest ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = True
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    await event.edit("Calculating my internet speed. Please wait!")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await event.edit(
                "**SpeedTest** completed in {} seconds\n"
                "Download: {}\n"
                "Upload: {}\n"
                "Ping: {}\n"
                "Internet Service Provider: {}\n"
                "ISP Rating: {}".format(
                    ms,
                    slitu.humanbytes(download_speed),
                    slitu.humanbytes(upload_speed),
                    ping_time,
                    i_s_p,
                    i_s_p_rating
                )
            ) 
        else:
            await borg.send_file(
                event.chat_id,
                speedtest_image,
                caption="**SpeedTest** completed in {} seconds".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False
            )
            await event.delete()
    except Exception as exc:
        await event.edit(
            "**SpeedTest** completed in {} seconds\n"
            "Download: {}\n"
            "Upload: {}\n"
            "Ping: {}\n\n"
            "__With the Following ERRORs__\n"
            "{}".format(
                ms,
                slitu.humanbytes(download_speed),
                slitu.humanbytes(upload_speed),
                ping_time,
                str(exc)
            )
        )

"""Get Poll Info on non supported clients
Syntax: .get_poll"""


@borg.on(slitu.admin_cmd(pattern="get_poll"))
async def _(event):
    reply_message = await event.get_reply_message()
    if reply_message.media is None or reply_message.media.poll is None:
        await event.edit(
            "Please reply to a media_type == @gPoll to view the questions and answers"
        )
    else:
        media = reply_message.media
        poll = media.poll
        closed_status = poll.closed
        answers = poll.answers
        question = poll.question
        edit_caption = f"Poll is Closed: {closed_status}\n"
        edit_caption += f"Question: {question}\n"
        edit_caption += "Answers: \n"
        if closed_status:
            results = media.results
            for i, result in enumerate(results.results):
                edit_caption += "{}> {}    {}\n".format(
                    result.option,
                    answers[i].text,
                    result.voters
                )
            edit_caption += "Total Voters: {}".format(results.total_voters)
        else:
            for answer in answers:
                edit_caption += "{}> {}\n".format(answer.option, answer.text)
        await event.edit(edit_caption)

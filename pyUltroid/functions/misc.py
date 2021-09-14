import aiohttp
from faker import Faker


# ---------------- Random User Gen ----------------
# @xditya


def get_random_user_data():
    base_url = "https://randomuser.me/api/"
    cc = Faker().credit_card_full().split("\n")
    card = (
        cc[0]
        + "\n"
        + "**CARD_ID:** "
        + cc[2]
        + "\n"
        + f"**{cc[3].split(':')[0]}:**"
        + cc[3].split(":")[1]
    )
    async with aiohttp.ClientSession() as ses:
        async with ses.get(base_url) as out:
            d = await out.json()
    data_ = d["results"][0]
    _g = data_["gender"]
    gender = "🤵🏻‍♂" if _g == "male" else "🤵🏻‍♀"
    name = data_["name"]
    loc = data_["location"]
    dob = data_["dob"]
    msg = """
{} **Name:** {}.{} {}
**Street:** {} {}
**City:** {}
**State:** {}
**Country:** {}
**Postal Code:** {}
**Email:** {}
**Phone:** {}
**Card:** {}
**Birthday:** {}
""".format(
        gender,
        name["title"],
        name["first"],
        name["last"],
        loc["street"]["number"],
        loc["street"]["name"],
        loc["city"],
        loc["state"],
        loc["country"],
        loc["postcode"],
        data_["email"],
        data_["phone"],
        card,
        dob["date"][:10],
    )
    pic = data_["picture"]["large"]
    return msg, pic

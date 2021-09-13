# py-Ultroid Library
A stable userbot base library, based on Telethon.

[![PyPI - Version](https://img.shields.io/pypi/v/py-Ultroid?style=for-the-badge)](https://pypi.org/project/py-Ultroid)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-Ultroid?label=DOWNLOADS&style=for-the-badge)](https://pypi.org/project/py-Ultroid)
[![The Ultroid](ultroid.svg)](https://t.me/TheUltroid)

## Installation
`pip install py-Ultroid`

## Usage
=> Create folders named `plugins`, `addons`, `assistant` and `resources`.<br/>
=> Add your plugins in the `plugins` folder and others accordingly.<br/>
=> Create a `.env` file with `API_ID`, `API_HASH`, `SESSION`, `REDIS_URI` & `REDIS_PASSWORD` as mandatory environment variables. Check
[`.env.sample`](https://github.com/TeamUltroid/Ultroid/blob/main/.env.sample) for more details.<br/>
=> Run `python -m pyUltroid` to start the bot.<br/>

### Creating plugins
To work everywhere

```python
@ultroid_cmd(
    pattern="start",
)   
async def _(e):   
    await eor(e, "Ultroid Started")   
```

To work only in groups

```python
@ultroid_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "Ultroid Started")   
```

Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("Ultroid Started")   
```

Made with 💕 by [@TeamUltroid](https://t.me/TeamUltroid). <br />


# License
Ultroid is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.

[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)

# Credits
* [![TeamUltroid-Devs](https://img.shields.io/static/v1?label=Teamultroid&message=devs&color=critical)](https://t.me/UltroidDevs)
* [Lonami](https://github.com/LonamiWebs) for [Telethon](https://github.com/LonamiWebs/Telethon)

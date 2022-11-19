# py-Ultroid Library

Core library of [The Ultroid](https://github.com/TeamUltroid/Ultroid), a python based telegram userbot.

[![CodeFactor](https://www.codefactor.io/repository/github/teamultroid/pyultroid/badge)](https://www.codefactor.io/repository/github/teamultroid/pyultroid)
[![PyPI - Version](https://img.shields.io/pypi/v/py-Ultroid?style=round)](https://pypi.org/project/py-Ultroid)    
[![PyPI - Downloads](https://img.shields.io/pypi/dm/py-Ultroid?label=DOWNLOADS&style=round)](https://pypi.org/project/py-Ultroid)    
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/TeamUltroid/Ultroid/graphs/commit-activity)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/TeamUltroid/Ultroid)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

# Installation
```bash
pip3 install -U py-Ultroid
```

# Documentation 
[![Documentation](https://img.shields.io/badge/Documentation-Ultroid-blue)](http://ultroid.tech/)

# Usage
- Create folders named `plugins`, `addons`, `assistant` and `resources`.   
- Add your plugins in the `plugins` folder and others accordingly.   
- Create a `.env` file with following mandatory Environment Variables
   ```
   API_ID
   API_HASH
   SESSION
   REDIS_URI
   REDIS_PASSWORD
   ```
- Check
[`.env.sample`](https://github.com/TeamUltroid/Ultroid/blob/main/.env.sample) for more details.   
- Run `python3 -m pyUltroid` to start the bot.   

## Creating plugins
 - ### To work everywhere

```python
@ultroid_cmd(
    pattern="start"
)   
async def _(e):   
    await e.eor("Ultroid Started!")   
```

- ### To work only in groups

```python
@ultroid_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "Ultroid Started.")   
```

- ### Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("Ultroid Started.")   
```

See more working plugins on [the offical repository](https://github.com/TeamUltroid/Ultroid)!

> Made with 💕 by [@TeamUltroid](https://t.me/TeamUltroid).    


# License
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)   
Ultroid is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.

# Credits
* [![TeamUltroid-Devs](https://img.shields.io/static/v1?label=TeamUltroid&message=devs&color=critical)](https://t.me/UltroidDevs)
* [Lonami](https://github.com/Lonami) for [Telethon](https://github.com/LonamiWebs/Telethon)

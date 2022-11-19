# uniborg

Pluggable [``asyncio``](https://docs.python.org/3/library/asyncio.html)
[Telegram](https://telegram.org) userbot based on
[Telethon](https://github.com/LonamiWebs/Telethon).


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
Mozilla Public License for more details.


## disclaimer

⚠️ This fork uses "requests" module in various places, instead of the async alternative. ⚠️

- This was an attempt to learn userbot development using Telethon, __this project is now no longer usable__, and is FORKed and MODIFied to suit MY needs, so **use at your own risk**.


## installing

#### The Easiest Way

- Install Docker by following the [official docker docs](https://docs.docker.com/engine/install/debian/)

- Start docker daemon [skip if already running]:
```sh
dockerd
```
- Build Docker image:
```sh
docker build . -t uniborg
```
- Run the image:
```sh
docker run uniborg
```

It is not recommended to use "sudo", while using Docker.
GNU/Linux Permissions are highly customisable, and it is generally not required to have "ROOT" permission, ~~unless you know what you are doing~~.
You can still install all the dependencies in your system [with ROOT permissions],
but please be aware of the potential issues when doing so. The installed packages
may conflict with the system package manager's installed packages, which can
cause trouble down the road and errors when upgrading conflicting packages.
**You have been warned.**

#### The Legacy Way
Simply clone the repository and run the main file:
```sh
git clone https://github.com/udf/uniborg.git
cd uniborg
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
cp sample_config.env config.env
# <edit config.env with appropriate values>
python3 -m kopp
```

## internals

The core features offered by the custom `TelegramClient` live under the
[`uniborg/`](https://github.com/SpEcHiDe/uniborg/tree/master/uniborg)
directory, with some utilities, enhancements, the `_core` plugin, and the `_inline_bot` plugin.

- Only five of the environment variables are mandatory.
- Please read the [WiKi](https://github.com/SpEcHiDe/UniBorg/wiki) to understand the use of the variables.
- This is because of `telethon.errors.ApiIdPublishedFloodError`
    - `APP_ID`: 
    - `API_HASH`:
    - `TG_BOT_TOKEN_BF_HER`: 
    - `TG_BOT_USER_NAME_BF_HER`: 
    - `DATABASE_URL`: 
- The userbot should work without setting the non-mandatory environment variables.


## design

The modular design of the project enhances your Telegram experience
through [plugins](https://github.com/SpEcHiDe/uniborg/tree/master/stdplugins)
which you can enable or disable on demand.

Each plugin gets the `borg`, `logger`, `Config` magical
[variables](https://github.com/spechide/UniBorg/blob/488eff632e65103ba7017d4f52777d22ddd52ea2/uniborg/uniborg.py#L76-L80)
to ease their use. Thus creating a plugin as easy as adding
a new file under the plugin directory to do the job:

```python
# stdplugins/myplugin.py
@borg.on(slitu.admin_cmd(pattern="hi"))
async def handler(event):
    await event.client.send_message(
        event.chat_id,
        "hey"
    )
```


## learning

Check out the already-mentioned [plugins](https://github.com/SpEcHiDe/UniBorg/tree/master/stdplugins) directory, or some third-party [plugins](https://telegram.dog/UniBorg) to learn how to write your own, and consider reading [Telethon's documentation](http://docs.telethon.dev/).


## credits


Thanks to:
- [lonami](https://lonami.dev) for creating [Telethon](https://github.com/lonamiwebs/Telethon)
- [![CopyLeft](https://telegra.ph/file/b514ed14d994557a724cb.jpg)](https://telegra.ph/file/fab1017e21c42a5c1e613.mp4 "CopyLeft Credit Video")

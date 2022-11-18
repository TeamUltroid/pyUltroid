

from Alexa.core.bot import AlexaBot
from Alexa.core.dir import dirr
from Alexa.core.git import git
from Alexa.core.userbot import Userbot
from Alexa.misc import dbb, heroku, sudo

from Alexa.logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()

# Bot Client
app = AlexaBot()

# Assistant Client
userbot = Userbot()

from Alexa.platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()

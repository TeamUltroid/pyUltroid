"""
import math
import os
import time
from mimetypes import guess_type

import httplib2
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from telethon import events

from .. import *
from .helper import humanbytes, time_formatter
"""


class GDriveManager:
    def __init__(self):
        self.gdrive_creds = {"oauth_scope": "https://www.googleapis.com/auth/drive", "mimetype": "application/vnd.google-apps.folder", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "redirect_uris": "urn:ietf:wg:oauth:2.0:oob"}

    def _authorise(self):
        something #todo
        

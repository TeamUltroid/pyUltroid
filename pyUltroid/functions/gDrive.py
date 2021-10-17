"""
import math
import os
import time
from mimetypes import guess_type

import httplib2
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from oauth2client.file import Storage
from telethon import events

from .. import *
from .helper import humanbytes, time_formatter
"""

from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from .. import udB


class GDriveManager:
    def __init__(self):
        self.gdrive_creds = {
            "oauth_scope": ["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive.metadata"],
            "mimetype": "application/vnd.google-apps.folder",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }
        self.auth_token = udB.get("GDRIVE_AUTH_TOKEN")

    def _authorise(self):
        self.flow = None
        if not self.flow:
            try:
                self.flow = OAuth2WebServerFlow(udB["GDRIVE_CLIENT_ID"], udB["GDRIVE_CLIENT_SECRET"], self.gdrive_creds["oauth_scope"], redirect_uri=self.gdrive_creds["redirect_uri"])
            except KeyError:
                some other function
            return self.flow.step1_get_authorize_url()
        else:
            return None

    def _verify_auth(self, token: str):
        _verified = None
        if self.flow:
            try:
                return self.flow.step2_exchange(token)
            except FlowExchangeError as e:
                return str(e)
        else:
            self._authorise()

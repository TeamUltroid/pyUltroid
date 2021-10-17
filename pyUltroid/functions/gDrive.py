"""
import math
import os
import time
from mimetypes import guess_type

import httplib2
from apiclient.http import MediaFileUpload
from telethon import events

from .. import *
from .helper import humanbytes, time_formatter
"""

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from httplib2 import Http
from googleapiclient.discovery import build


from .. import udB

_auth_flow = None


class GDriveManager:
    def __init__(self):
        self.gdrive_creds = {
            "oauth_scope": [
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive.metadata",
            ],
            "mimetype": "application/vnd.google-apps.folder",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }
        self.auth_token = udB.get("GDRIVE_AUTH_TOKEN")
        self.token_file = "resources/auth/gdrive_creds.json"
        self.build = build("drive", "v2", http=self._http(), cache_discovery=False)


    def _create_token_file(
        self, code: str = None
    ):
        global _auth_flow
        if code and _auth_flow:
            credentials = _auth_flow.step2_exchange(code)
            storage = Storage(self.token_file).put(credentials)
            return udB.set_redis("GDRIVE_AUTH_TOKEN", open(self.token_file).read())
        try:
            _auth_flow = OAuth2WebServerFlow(
                udB["GDRIVE_CLIENT_ID"],
                udB["GDRIVE_CLIENT_SECRET"],
                self.gdrive_creds["oauth_scope"],
                redirect_uri=self.gdrive_creds["redirect_uri"],
            )
        except KeyError:
            return "Fill GDRIVE client credentials"
        return _auth_flow.step1_get_authorize_url()

    def _http(self):
        storage = Storage(self.token_file).get()
        http = Http()
        storage.refresh(http)
        return http

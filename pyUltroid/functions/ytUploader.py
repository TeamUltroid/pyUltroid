from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.client import OOB_CALLBACK_URN, OAuth2WebServerFlow
from oauth2client.file import Storage

from .. import udB

_auth_flow = None


class YouTubeUploader:
    def __init__(self):
        self.yt_creds = {
            "oauth_scope": [
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube",
            ],
            "redirect_uri": OOB_CALLBACK_URN,
        }
        self.auth_token = udB.get("YT_AUTH_TOKEN")
        self.token_file = "resources/auth/yt_creds.json"

    def _create_token_file(self, code: str = None):
        global _auth_flow
        if code and _auth_flow:
            credentials = _auth_flow.step2_exchange(code)
            Storage(self.token_file).put(credentials)
            return udB.set("YT_AUTH_TOKEN", str(open(self.token_file).read()))
        try:
            _auth_flow = OAuth2WebServerFlow(
                udB["YT_CLIENT_ID"],
                udB["YT_CLIENT_SECRET"],
                self.yt_creds["oauth_scope"],
                redirect_uri=self.yt_creds["redirect_uri"],
            )
        except KeyError:
            return "Fill YouTube client credentials"
        return _auth_flow.step1_get_authorize_url()

    def _http(self):
        storage = Storage(self.token_file)
        creds = storage.get()
        http = Http()
        http.redirect_codes = http.redirect_codes - {308}
        creds.refresh(http)
        return creds.authorize(http)

    def _build(self):
        return build("youtube", "v3", http=self._http())

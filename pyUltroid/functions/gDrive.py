import time
from io import FileIO
from mimetypes import guess_type

from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.client import OOB_CALLBACK_URN, OAuth2WebServerFlow
from oauth2client.file import Storage

from .. import udB
from .helper import progress

_auth_flow = None


class GDriveManager:
    def __init__(self):
        self.gdrive_creds = {
            "oauth_scope": [
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive.metadata",
            ],
            "dir_mimetype": "application/vnd.google-apps.folder",
            "redirect_uri": OOB_CALLBACK_URN,
        }
        self.auth_token = udB.get("GDRIVE_AUTH_TOKEN")
        self.folder_id = udB.get("GDRIVE_FOLDER_ID")
        self.token_file = "resources/auth/gdrive_creds.json"

    def _create_token_file(self, code: str = None):
        global _auth_flow
        if code and _auth_flow:
            credentials = _auth_flow.step2_exchange(code)
            Storage(self.token_file).put(credentials)
            return udB.set("GDRIVE_AUTH_TOKEN", str(open(self.token_file).read()))
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
        storage = Storage(self.token_file)
        creds = storage.get()
        http = Http()
        http.redirect_codes = http.redirect_codes - {308}
        creds.refresh(http)
        return creds.authorize(http)

    def _build(self):
        return build("drive", "v2", http=self._http(), cache_discovery=False)

    def _set_permissions(self, fileId: str):
        _permissions = {
            "role": "reader",
            "type": "anyone",
        }
        self._build().permissions().insert(
            fileId=fileId, body=permissions, supportsAllDrives=True
        ).execute(http=self._http())

    async def _upload_file(self, event, path: str, filename: str = None):
        if not filename:
            filename = path.split("/")[-1]
        mime_type = guess_type(path)[0] or "application/octet-stream"
        media_body = MediaFileUpload(path, mimetype=mime_type, resumable=True)
        body = {
            "title": filename,
            "description": "Uploaded using Ultroid Userbot",
            "mimeType": mime_type,
        }
        if self.folder_id:
            body["parents"] = [{"id": self.folder_id}]
        upload = (
            self._build()
            .files()
            .insert(body=body, media_body=media_body, supportsAllDrives=True)
        )
        start = time.time()
        _status = None
        while not _status:
            _progress, _status = upload.next_chunk(num_retries=3)
            if _progress:
                uploaded = _progress.resumable_progress
                total_size = _progress.total_size
                await progress(
                    uploaded,
                    total_size,
                    event,
                    start,
                    f"Uploading {filename} on GDrive...",
                )
        fileId = _status.get("id")
        try:
            self._set_permissions(fileId=fileId)
        except BaseException:
            pass
        _url = (
            self._build().files().get(fileId=fileId, supportsTeamDrives=True).execute()
        )
        return _url.get("webContentLink")

    async def _download_file(self, event, fileId: str, filename: str = None):
        if fileId.startswith("http"):
            if fileId.endswith("=download"):
                fileId = fileId.split("=")[1]
            elif fileId.endswith("/view"):
                fileId = fileId.split("/")[::-1][1]
        else:
            pass
        if not filename:
            filename = self._build().files().get(fileId=fileId).execute()["title"]
        downloader = (
            self._build().files().get_media(fileId=fileId, supportsTeamDrives=True)
        )
        with FileIO(filename, "wb") as file:
            start = time.time()
            download = MediaIoBaseDownload(file, downloader)
            _status = None
            while not _status:
                _progress, _status = download.next_chunk(num_retries=3)
                if _progress:
                    uploaded = _progress.resumable_progress
                    total_size = _progress.total_size
                    await progress(
                        uploaded,
                        total_size,
                        event,
                        start,
                        f"Downloading {filename} on GDrive...",
                    )

    def _list_files(self):
        _items = self._build().files().get(fileId="", supportsTeamDrives=True).execute()
        _files = {}
        for files in _items["items"]:
            try:
                _files[files["webContentLink"]] = files["title"]
            except KeyError:
                pass
        return _files

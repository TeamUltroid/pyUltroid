from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from . import *


class GDriveManager:
    def __init__(self):
        self.GoogleAuth = GoogleAuth()
        self.GoogleDrive = GoogleDrive(self.GoogleAuth)

    def _generate_auth_url(self):
        return self.GoogleAuth.GetAuthUrl()

    def _authorise(self, token: str):
        self.GoogleAuth.Auth(token)

    def _save_credentials_file(
        self, path_to_file: str = "./resources/auth/client_secrets.json"
    ):
        self.SaveCredentialsFile(path_to_file)
        with open(path_to_file, "r") as f:
            udB.set_redis("GDRIVE_AUTH_TOKEN", f.read())

    def _login(self, path_to_file: str = "./resources/auth/client_secrets.json"):
        try:
            self.LoadCredentialsFile(path_to_file)
            return "Success"
        except Exception as e:
            print(e)
            return "Error"

    def _initialize_cs_json(
        self, path_to_file: str = "./resources/auth/client_secrets.json"
    ):
        _json = {
            "installed": {
                "client_id": udB.get("GDRIVE_CLIENT_ID"),
                "client_secret": udB.get("GDRIVE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
                "save_credentials": True,
                "access_type": "offline",
            }
        }
        with open(path_to_file, "w") as f:
            f.write(str(_json).replace("'", '"').replace("True", "true"))

    def _upload_file(self, path_to_file: str, file_name: str):
        folder_id = udB.get("GDRIVE_FOLDER_ID")
        if folder_id:
            try:
                the_file = self.GoogleDrive.CreateFile(
                    {
                        "title": file_name,
                        "parents": [{"kind": "drive#fileLink", "id": folder_id}],
                    }
                )
                the_file.SetContentFile(path_to_file)
                the_file.Upload()
                return "Uploaded Successfully"
            except ApiRequestError as e:
                if e.GetField("reason") == "notFound":
                    return "Gdrive folder not found"

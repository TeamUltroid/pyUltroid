from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GDriveManager:
    def __init__(self):
        self.GoogleAuth = GoogleAuth()
        self.GoogleDrive = GoogleDrive(self.GoogleAuth)

    def _generate_auth_url(self):
        return self.GoogleAuth.GetAuthUrl()

    def _authorise(self, token: str):
        self.GoogleAuth.Auth(token)

import os
from dotenv import load_dotenv
import dropbox

class TrasnferData:
    def __init__(self, access_token):
        self.access_token = access_token
    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, "rb") as f:
            dbx.files_upload(f.read(), file_to)

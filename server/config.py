import datetime
import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    def __init__(self):
        self.datetime_format = "%Y-%m-%d %H:%M:%S"
        self.iam_token = os.getenv('IAM_TOKEN')
        self.oauth_token = os.getenv('OAUTH_TOKEN')
        self.update_time = datetime.datetime.strptime(os.getenv('UPDATE_TIME'), self.datetime_format)
        self.folder_id = os.getenv('FOLDER_ID')
        self.target_language = 'ru'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.iam_token)
        }

    def update_token(self, iam_token, update_time: datetime.datetime):
        self.iam_token = iam_token
        self.update_time = update_time
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.iam_token)
        }


config = Config()

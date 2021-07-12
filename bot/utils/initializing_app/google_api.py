from google.oauth2.service_account import Credentials
from .config import config


def get_google_api_credentials():
    return Credentials.from_service_account_file(
        config.service_account_file_path
    ).with_scopes([
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])

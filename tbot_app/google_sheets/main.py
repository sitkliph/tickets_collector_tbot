"""Interface for Google Sheets API."""
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

from google_sheets import settings
from google_sheets.utils import make_ticket_info


load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file(
    os.getenv('GOOGLE_API_JSON_KEY_PATH'),
    scopes=SCOPES
)
client = gspread.authorize(credentials)
table = client.open_by_key(settings.TABLE_ID)
worksheet = table.worksheet(settings.WORKSHEET_TITLE)


def insert_ticket_info(ticket: dict) -> None:
    """
    Insert ticket's information into Google Sheets.

    :param ticket_info: Ticket's values to insert into table.
    """
    worksheet.append_row(make_ticket_info(ticket))

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("config/signofdestinybot.json", scope)
client = gspread.authorize(creds)

sheet = client.open("SignOfDestinyBot").sheet1

def export_mood_to_sheet(user_id: str, mood: str, description: str, timestamp: str):
    timestamp = datetime.fromisoformat(timestamp).strftime("%d.%m.%Y %H:%M")
    row = [
        str(user_id),
        mood,
        description if description else "",
        timestamp
    ]
    sheet.append_row(row)
    # sheet.append_row([user_id, mood, description, timestamp])

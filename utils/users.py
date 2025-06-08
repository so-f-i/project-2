import json
from pathlib import Path

USER_IDS_FILE = Path("storage/user_ids.json")
BANNED_USERS_FILE = Path("storage/banned_users.json")

def get_all_user_ids():
    if USER_IDS_FILE.exists():
        with open(USER_IDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def ban_user(user_id: str):
    if BANNED_USERS_FILE.exists():
        with open(BANNED_USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data[str(user_id)] = True

    with open(BANNED_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def unban_user(user_id: str):
    if not BANNED_USERS_FILE.exists():
        return

    with open(BANNED_USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if str(user_id) in data:
        del data[str(user_id)]

    with open(BANNED_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ini.env")
load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))

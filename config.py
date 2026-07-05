import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TEMP_DIR = "temp_placeholders"
DB_NAME = "placegen.db"

import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
DB_PATH = "db/bookings.db"

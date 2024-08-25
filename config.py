# root.config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database configuration
DB_PATH = os.getenv('DB_PATH', 'tasks.db')
if not DB_PATH:
    raise ValueError("DB_PATH environment variable is not set")

# Database table and field names
TASKS_TABLE = "tasks"
DEFAULT_STATUS = "Pending"

# GUI configuration
WINDOW_TITLE = "HMH: Henry's Molok Hanterare"
WINDOW_SIZE = (800, 600)
HOME_PAGE_WELCOME_MSG = """ """
FONT_SETTINGS = {
    "default": ("Arial", 16, True),  # Font family, size, bold
    "color": "#2E8B57"
}

# Add additional settings here as needed

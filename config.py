# root.config.py
import os
from dotenv import load_dotenv


load_dotenv()

DB_PATH = os.getenv('DB_PATH', 'default_value.db')

if not DB_PATH:
    raise ValueError("DB_PATH environment variable is not set")

# Database table and field names
ASSIGNMENTS_TABLE = "assignments"
DEFAULT_STATUS = "Pending"

# GUI settings
WINDOW_TITLE = "HMH: Henry's Molok Hanterare"
WINDOW_SIZE = (800, 600)
HOME_PAGE_WELCOME_MSG = """Välkommen till Henry's Molok Hanterare
    , eller HMH (Patent pending)"""
FONT_SETTINGS = {
    "default": ("Arial", 16, True),  # Font family, size, bold
    "color": "#2E8B57"
}

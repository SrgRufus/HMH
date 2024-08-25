# root.__init__.py

# Optionally, you can import modules or packages here
from .config import DB_PATH, TASKS_TABLE, DEFAULT_STATUS
from .main import main

__all__ = ['DB_PATH', 'TASKS_TABLE', 'DEFAULT_STATUS', 'main']

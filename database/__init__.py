# database/__init__.py

from .db_manager import DBManager
from .models import Base, Task
from .operations import execute_query, batch_insert
from .connection import Session, init_db, get_db_connection, engine, scoped_session_instance
from .managers import TaskManager, TaskFetcher, TaskStatusManager, EventManager, RecurrenceManager
from .history_model import TaskHistory
# Explicitly exposing connection and models modules
from . import connection
from . import models

__all__ = [
    'DBManager',
    'Base',
    'Task',
    'execute_query',
    'batch_insert',
    'init_db',
    'get_db_connection',
    'engine',
    'scoped_session_instance',
    'TaskManager',
    'TaskFetcher',
    'TaskStatusManager',
    'EventManager',
    'RecurrenceManager',
    'connection',  # Exposing the connection module
    'models',
    'Session',# Exposing the models module
    'TaskHistory',
]

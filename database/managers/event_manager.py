# database/managers/event_manager.py
import logging

from handlers import CentralEventHandler
from .. import connection  # Import connection module
from .. import models  # Import models module


# Use centralized session from connection.py
# Use Task model from models.py


class EventManager:
    def __init__(self, recurrence_manager):
        self.session = connection.scoped_session_instance()
        self.recurrence_manager = recurrence_manager
        self.event_handler = CentralEventHandler()

    def setup_handlers(self):
        """Register event handlers."""
        self.event_handler.register_handler('task_completed', self.handle_task_completed)

    def handle_task_completed(self, task: models.Task):
        """Handle the task completed event by creating a recurring task."""
        try:
            self.recurrence_manager.create_recurring_task(task, recurrence_interval_days=7)
        except Exception as e:
            logging.error(f"Error handling task completed event: {e}")

    def insert_task(self, task: models.Task):
        """Insert a task and trigger a task created event."""
        self.session.add(task)
        self.session.commit()
        try:
            self.event_handler.trigger_event('task_created', task)
        except Exception as e:
            logging.error(f"Error triggering task created event: {e}")

    def close(self):
        self.session.close()

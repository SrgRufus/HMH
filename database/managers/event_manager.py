# database.managers.event_manager.py : Kombinerar återkommande logik med eventhantering.
from database.connection import Session as DBSession
from handlers.central_event_handler import event_handler, CentralEventHandler
from database.models import Task


class EventManager:
    def __init__(self, recurrence_manager):
        self.session = DBSession()
        self.recurrence_manager = recurrence_manager
        self.event_handler = CentralEventHandler()


    def setup_handlers(self):
        """Register event handlers."""
        self.event_handler.register_handler('task_completed', self.handle_task_completed)


    def handle_task_completed(self, task: Task):
        """Handle the task completed event by creating a recurring task."""
        try:
            self.recurrence_manager.create_recurring_task(task, recurrence_interval_days=7)
        except Exception as e:
            print(f"Error handling task completed event: {e}")


    def insert_task(self, task: Task):
        """Insert a task and trigger a task created event."""
        self.session.add(task)
        self.session.commit()
        try:
            event_handler.trigger_event('task_created', task)
        except Exception as e:
            print(f"Error triggering task created event: {e}")


    def close(self):
        self.session.close()

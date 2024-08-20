# database.managers.event_manager.py : Kombinerar återkommande logik med eventhantering.
from handlers.central_event_handler import event_handler, CentralEventHandler
from database.managers.recurrence_manager import RecurrenceManager


class EventManager:
    def __init__(self, db_path: str, recurrence_manager: RecurrenceManager) -> None:
        self.db_path = db_path
        self.recurrence_manager = recurrence_manager
        self.event_handler = CentralEventHandler

    def setup_handlers(self) -> None:
        self.event_handler.register_handler('task_completed', self.handle_task_completed)

    def handle_task_completed(self, task):
        self.recurrence_manager.create_recurring_task(task, recurrence_interval_days=7)

        # Log task creation for testing/debugging
    @staticmethod
    def log_task_creation(task):
        print(f"Task created: {task}")

    # Ta bort log_task och notify_user efter utveckling
        # Notify user about the task for testing/debugging
    @staticmethod
    def notify_user(task):
        print(f"Notification sent for assignment: {task}")

    def insert_task(self, task):
        self.log_task_creation(task)
        self.notify_user(task)
        # Trigger task creation event
        event_handler.trigger_event('task_created', task)

# database.managers.event_manager.py : Kombinerar återkommande logik med eventhantering.
from handlers.central_event_handler import event_handler, CentralEventHandler
from database.managers.recurrence_manager import RecurrenceManager


class EventManager:
    def __init__(self, db_path: str, recurrence_manager: RecurrenceManager) -> None:
        self.db_path = db_path
        self.recurrence_manager = recurrence_manager
        self.event_handler = CentralEventHandler

    def setup_handlers(self) -> None:
        self.event_handler.register_handler('assignment_completed', self.handle_assignment_completed)

    def handle_assignment_completed(self, assignment):
        self.recurrence_manager.create_recurring_assignment(assignment, recurrence_interval_days=7)

        # Log assignment creation for testing/debugging
    @staticmethod
    def log_assignment_creation(assignment):
        print(f"Assignment created: {assignment}")

    # Ta bort log_assignment och notify_user efter utveckling
        # Notify user about the assignment for testing/debugging
    @staticmethod
    def notify_user(assignment):
        print(f"Notification sent for assignment: {assignment}")

    def insert_assignment(self, assignment):
        self.log_assignment_creation(assignment)
        self.notify_user(assignment)
        # Trigger assignment creation event
        event_handler.trigger_event('assignment_created', assignment)

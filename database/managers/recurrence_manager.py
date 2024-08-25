# database/managers/recurrence_manager.py
from datetime import timedelta

from utils import validate_and_parse_date
from .. import connection  # Import connection module
from .. import models  # Import models module


# Use centralized session from connection.py
# Use Task model from models.py


class RecurrenceManager:
    def __init__(self):
        self.session = connection.scoped_session_instance()

    @staticmethod
    def calculate_recurring_task(task, recurrence_interval_days):
        # Validate and parse the next occurrence date
        task.next_occurrence_date = validate_and_parse_date(task.next_occurrence_date)
        # Calculate the next date based on recurrence interval
        next_date = task.next_occurrence_date + timedelta(days=recurrence_interval_days)
        # Create a new task with updated next occurrence date
        new_task = models.Task(
            kommun=task.kommun,
            adress=task.adress,
            ort=task.ort,
            material=task.material,
            tomningsfrekvens=task.tomningsfrekvens,
            info=task.info,
            chauffor=task.chauffor,
            koordinater=task.koordinater,
            next_occurrence_date=next_date
        )
        return new_task

    def create_and_add_recurring_task(self, task, recurrence_interval_days, event_manager):
        # Use the method to calculate and create a recurring task
        new_task = self.calculate_recurring_task(task, recurrence_interval_days)
        # Insert the new task into the database and trigger an event
        event_manager.insert_task(new_task)
        event_manager.event_handler.trigger_event('task_created', new_task)

    def close(self):
        # Close the session when done
        self.session.close()

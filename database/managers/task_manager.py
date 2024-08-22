# database.managers.task_manager.py
from datetime import datetime
from database.connection import Session as DBSession
from database.models import Task
from utils.date_utils import validate_and_parse_date


class TaskManager:
    def __init__(self):
        self.session = DBSession()


    def create_task(self, kommun, adress, ort, material, tomningsfrekvens, info, chauffor, koordinater, next_occurrence_date):
        next_occurrence_date = validate_and_parse_date(next_occurrence_date)
        new_task = Task(
            kommun=kommun,
            adress=adress,
            ort=ort,
            material=material,
            tomningsfrekvens=tomningsfrekvens,
            info=info,
            chauffor=chauffor,
            koordinater=koordinater,
            next_occurrence_date=next_occurrence_date
        )
        self.session.add(new_task)
        self.session.commit()

    def fetch_task_by_id(self, task_id):
        """Fetch a task by its ID."""
        return self.session.query(Task).get(task_id)

    def update_task_status(self, task_id, status, image_path=None):
        task = self.session.query(Task).get(task_id)
        if task:
            task.status = status
            if image_path:
                task.image_path = image_path
            self.session.commit()


    def get_tasks_for_date(self, date):
        return self.session.query(Task).filter(Task.next_occurrence_date == date).all()


    def delete_task(self, task_id):
        task = self.session.query(Task).get(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()

    @staticmethod
    def sort_tasks(tasks):
        today = datetime.today().date()

        def sort_key(task):
            next_date = task.next_occurrence_date.date()
            if next_date < today:
                return 0, next_date  # Overdue tasks first
            elif next_date == today:
                return 1, next_date  # Today's tasks next
            else:
                return 2, next_date  # Future tasks last

        return sorted(tasks, key=sort_key)

    def close(self):
        self.session.close()

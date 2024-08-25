# database/managers/task_fetcher.py
from functools import lru_cache

from .. import connection  # Import connection module
from .. import models  # Import models module


# Use centralized session from connection.py
# Use Task model from models.py


class TaskFetcher:
    def __init__(self):
        self.session = connection.scoped_session_instance()

    def fetch_all_tasks(self, page_num=1, page_size=20):
        """Fetch tasks with pagination support."""
        return self.session.query(models.Task).limit(page_size).offset((page_num - 1) * page_size).all()

    @lru_cache(maxsize=128)
    def fetch_tasks_sorted_by_date(self):
        """Fetch tasks sorted by their next occurrence date, with caching."""
        return self.session.query(models.Task).order_by(models.Task.next_occurrence_date.asc()).all()

    def fetch_tasks_for_current_week(self, start_of_week, end_of_week):
        """Fetch tasks for the current week."""
        return self.session.query(models.Task).filter(models.Task.next_occurrence_date.between(start_of_week, end_of_week)).all()

    def fetch_task_by_id(self, task_id):
        """Fetch a single task by its ID."""
        return self.session.query(models.Task).get(task_id)

    def close(self):
        self.session.close()


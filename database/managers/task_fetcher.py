# database.managers.task_fetcher.py
from database.models import Task
from database.connection import Session as DBSession
from functools import lru_cache


class TaskFetcher:
    def __init__(self):
        self.session = DBSession()

    def fetch_all_tasks(self, page_num=1, page_size=20):
        """Fetch tasks with pagination support."""
        return self.session.query(Task).limit(page_size).offset((page_num - 1) * page_size).all()

    @lru_cache(maxsize=128)
    def fetch_tasks_sorted_by_date(self):
        """Fetch tasks sorted by their next occurrence date, with caching."""
        return self.session.query(Task).order_by(Task.next_occurrence_date.asc()).all()

    def fetch_tasks_for_current_week(self, start_of_week, end_of_week):
        """Fetch tasks for the current week."""
        return self.session.query(Task).filter(Task.next_occurrence_date.between(start_of_week, end_of_week)).all()

    def fetch_task_by_id(self, task_id):
        """Fetch a single task by its ID."""
        return self.session.query(Task).get(task_id)

    def close(self):
        self.session.close()


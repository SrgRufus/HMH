# database.managers.task_fetcher.py
from database.queries.assignment_queries import (
    SELECT_ALL_TASKS, SELECT_TASKS_SORTED_BY_DATE, SELECT_TASKS_FOR_CURRENT_WEEK,
    SELECT_TASK_BY_ID
)
from database.models import Task
from database.operations import fetch_all
from database.connection import get_db_connection


class TaskFetcher:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def fetch_all_tasks(self):
        rows = fetch_all(self.db_path, SELECT_ALL_TASKS)
        return [Task(*row) for row in rows]

    def fetch_tasks_sorted_by_date(self):
        rows = fetch_all(self.db_path, SELECT_TASKS_SORTED_BY_DATE)
        return [Task(*row) for row in rows]

    def fetch_tasks_for_current_week(self, start_of_week, end_of_week):
        rows = fetch_all(self.db_path, SELECT_TASKS_FOR_CURRENT_WEEK, (start_of_week, end_of_week))
        return [Task(*row) for row in rows]

    def fetch_task_by_id(self, assignment_id):
        with get_db_connection(self.db_path) as connection:
            cursor = connection.cursor()
            query = SELECT_TASK_BY_ID
            cursor.execute(query, (assignment_id,))
            cursor.fetchone()
            # Fortsätt bearbeta datan här

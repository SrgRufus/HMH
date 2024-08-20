# database.managers.assignment_status_manager.py
from database.queries.task_queries import UPDATE_JOB_STATUS
from database.operations import execute_query

class TaskStatusManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def update_job_status(self, task_id, status, image_path=None):
        execute_query(self.db_path, UPDATE_JOB_STATUS, (status, image_path, task_id))

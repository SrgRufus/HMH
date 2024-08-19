# database.managers.assignment_status_manager.py
from database.managers.queries.assignment_queries import UPDATE_JOB_STATUS
from database.operations import execute_query

class AssignmentStatusManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def update_job_status(self, assignment_id, status, image_path=None):
        execute_query(self.db_path, UPDATE_JOB_STATUS, (status, image_path, assignment_id))

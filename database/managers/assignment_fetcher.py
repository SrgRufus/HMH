# database.managers.assignment_fetcher.py
from database.managers.queries.assignment_queries import (
    SELECT_ALL_ASSIGNMENTS, SELECT_ASSIGNMENTS_SORTED_BY_DATE, SELECT_ASSIGNMENTS_FOR_CURRENT_WEEK,
    SELECT_ASSIGNMENT_BY_ID
)
from database.models import Assignment
from database.operations import fetch_all
from database.connection import get_db_connection


class AssignmentFetcher:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def fetch_all_assignments(self):
        rows = fetch_all(self.db_path, SELECT_ALL_ASSIGNMENTS)
        return [Assignment(*row) for row in rows]

    def fetch_assignments_sorted_by_date(self):
        rows = fetch_all(self.db_path, SELECT_ASSIGNMENTS_SORTED_BY_DATE)
        return [Assignment(*row) for row in rows]

    def fetch_assignments_for_current_week(self, start_of_week, end_of_week):
        rows = fetch_all(self.db_path, SELECT_ASSIGNMENTS_FOR_CURRENT_WEEK, (start_of_week, end_of_week))
        return [Assignment(*row) for row in rows]

    def fetch_assignment_by_id(self, assignment_id):
        with get_db_connection(self.db_path) as connection:
            cursor = connection.cursor()
            query = SELECT_ASSIGNMENT_BY_ID
            cursor.execute(query, (assignment_id,))
            cursor.fetchone()
            # Fortsätt bearbeta datan här

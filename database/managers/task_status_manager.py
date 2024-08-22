# database.managers.task_status_manager.py
from database.models import Task
from database.connection import Session as DBSession

class TaskStatusManager:
    def __init__(self):
        self.session = DBSession()

    def update_task_status(self, task_id, status, image_path=None):
        """Uppdatera status på uppdraget, valmöjlighet finns att ladda upp bild."""
        valid_statuses = ["Pending", "In Progress", "Completed", "Failed"]  # Example statuses
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}")

        task = self.session.query(Task).get(task_id)
        if task:
            task.status = status
            if image_path:
                task.image_path = image_path
            self.session.commit()
        else:
            raise ValueError(f"Task with ID {task_id} not found.")

    def close(self):
        self.session.close()

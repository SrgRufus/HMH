# database/managers/task_status_manager.py
from .. import connection  # Import connection module
from .. import models  # Import models module


# Use centralized session from connection.py
# Use Task model from models.py



class TaskStatusManager:
    def __init__(self):
        self.session = connection.scoped_session_instance()

    def update_task_status(self, task_id, status, image_path=None):
        """Uppdatera status på uppdraget, valmöjlighet finns att ladda upp bild."""
        valid_statuses = ["Pending", "In Progress", "Completed", "Failed"]  # Example statuses
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}")

        task = self.session.query(models.Task).get(task_id)
        if task:
            task.status = status
            if image_path:
                task.image_path = image_path
            self.session.commit()
        else:
            raise ValueError(f"Task with ID {task_id} not found.")

    def close(self):
        self.session.close()

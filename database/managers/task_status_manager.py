# database/managers/task_status_manager.py
from database import connection, Task

class TaskStatusManager:
    def __init__(self):
        """Konstruktor för TaskStatusManager som initierar en trådsäker session."""
        self.session = connection.scoped_session_instance()

    def update_task_status(self, task_id, status, image_path=None):
        """
        Uppdaterar statusen för en uppgift och, om tillämpligt, dess bildväg.
        :param task_id: ID för uppgiften som ska uppdateras.
        :param status: Ny status för uppgiften.
        :param image_path: Sökvägen till en bild relaterad till uppgiften (valfritt).
        """
        with self.session as session:
            task = session.query(Task).get(task_id)  # Hämta uppgiften baserat på ID
            if task:
                task.status = status  # Uppdatera statusen
                if image_path:
                    task.image_path = image_path  # Uppdatera bildvägen om den angavs
                session.commit()  # Utför commit för att spara ändringarna
            else:
                raise ValueError(f"Task with ID {task_id} not found.")  # Kasta ett fel om uppgiften inte hittas

    def close(self):
        """Stänger databassessionen."""
        self.session.close()


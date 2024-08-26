# controllers/task_controller.py
import logging  # Importera logging för att hålla koll på vad som händer i koden

from database.managers.task_manager import TaskManager  # Importera TaskManager för att hantera uppgifter i databasen


class TaskController:
    def __init__(self, session):
        """När det skapas ett TaskController-objekt, initieras TaskManager som tar hand om uppgifterna."""
        self.task_manager = TaskManager(session)  # Här skickas sessionen till TaskManager
        logging.basicConfig(level=logging.DEBUG)  # Sätter upp logging så att man kan se vad som händer, särskilt för att felsöka

    def fetch_all_tasks(self):
        """Den här metoden hämtar alla uppgifter från databasen och returnerar dem."""
        return self.task_manager.get_all_tasks()

    def fetch_task_by_id(self, task_id: int):
        """Den här metoden hämtar en specifik uppgift från databasen baserat på dess ID."""
        try:
            return self.task_manager.fetch_task_by_id(task_id)
        except Exception as e:
            logging.error(f"Error fetching task by ID {task_id}: {e}")  # Loggar ett fel om något går snett
            return None

    def update_task(self, task_id: int, updated_data: dict) -> bool:
        """Den här metoden uppdaterar en uppgift med de nya uppgifterna som skickas in."""
        try:
            success = self.task_manager.update_task_status(task_id, updated_data)  # Försöker uppdatera uppgiften
            if success:
                logging.info("Task updated successfully.")  # Loggar framgång om uppdateringen lyckades
            return success
        except Exception as e:
            logging.error(f"Error updating task: {e}")  # Loggar ett fel om något går snett
            return False

# controller.task_controller.py : Enhanced error handling and validation
import logging
from database import TaskManager
from utils import validate_task_data # Lägg till denna rad för att använda din valideringsfunktion

class TaskController:
    def __init__(self):
        self.task_manager = TaskManager()
        logging.basicConfig(level=logging.INFO)  # Configure logging

    def create_task(self, data: dict) -> bool:
        """
        Create a task with the provided data after validation.
        :param data: Dictionary containing task details.
        :return: True if the task is created successfully, False otherwise.
        """
        try:
            validate_task_data(data['tomningsfrekvens'])  # Validera frekvensen
            # Skapa uppdraget och validerade data
            self.task_manager.create_task(
                kommun=data['kommun'],
                adress=data['adress'],
                ort=data['ort'],
                material=data['material'],
                tomningsfrekvens=data['tomningsfrekvens'],
                info=data.get('info', ''),
                chauffor=data.get('chauffor', ''),
                koordinater=data.get('koordinater', ''),
                next_occurrence_date=data['next_occurrence_date']
            )
            logging.info("Task created successfully.")
            return True
        except ValueError as e:
            logging.error(f"Validation Error: {e}")
            return False
        except Exception as e:
            logging.error(f"Error creating task: {e}")
            return False

    def get_tasks_for_date(self, date):
        return self.task_manager.get_tasks_by_date(date)

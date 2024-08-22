# controller.task_controller.py : Enhanced error handling and validation
from database.managers.task_manager import TaskManager
from utils.task_utils import validate_task_data # Lägg till denna rad för att använda din valideringsfunktion

class TaskController:
    def __init__(self):
        self.task_manager = TaskManager()

    def create_task(self, data):
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
            return True
        except ValueError as e:
            print(f"Validation Error: {e}")
            return False
        except Exception as e:
            print(f"Error creating task: {e}")
            return False

    def get_tasks_for_date(self, date):
        return self.task_manager.get_tasks_by_date(date)

# database.managers.task_manager.py
from black import datetime
from database.managers.task_fetcher import TaskFetcher
from database.connection import get_db_connection
from handlers.central_event_handler import event_handler

class TaskManager:
    def __init__(self, db_path: str, event_manager) -> None:
        self.db_path = db_path
        self.event_manager = event_manager
        self.fetcher = TaskFetcher(self.db_path)  # Kontrollera att denna attribut är korrekt instanserad

    def create_task(self, kommun, adress, ort, material, tomningsfrekvens, info, chauffor, koordinater, next_occurrence_date):
        query = """
            INSERT INTO task (kommun, adress, 
                                     ort, material,
                                     tomningsfrekvens, info, 
                                     chauffor, koordinater, 
                                     next_occurrence_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        params = (kommun, adress, ort, material, tomningsfrekvens, info, chauffor, koordinater, next_occurrence_date.strftime('%Y-%m-%d'))

        # Använd en kontextmanager för att hantera anslutningen
        with get_db_connection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, params)
                connection.commit()

                # Definiera data för eventet
                data = {
                    'kommun': kommun,
                    'adress': adress,
                    'ort': ort,
                    'material': material,
                    'tomningsfrekvens': tomningsfrekvens,
                    'info': info,
                    'chauffor': chauffor,
                    'koordinater': koordinater,
                    'next_occurrence_date': next_occurrence_date.strftime('%Y-%m-%d')
                }

                # Trigga händelsen efter att uppdraget har skapats
                event_handler.trigger_event('task_created', data)

            except Exception as e:
                raise RuntimeError(f"Fel vid skapande av uppdrag: {e}")

    def fetch_all_tasks(self):
        return self.fetcher.fetch_all_tasks()

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        with get_db_connection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (task_id,))
                connection.commit()
            except Exception as e:
                raise RuntimeError(f"Fel vid borttagning av uppdrag: {e}")

    def fetch_task_by_id(self, task_id):
        query = "SELECT * FROM tasks WHERE id = ?"
        with get_db_connection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (task_id,))
                row = cursor.fetchone()
                if row:
                    return row
                else:
                    raise RuntimeError("Uppdraget kunde inte hittas.")
            except Exception as e:
                raise RuntimeError(f"Fel vid hämtning av uppdrag: {e}")

    def update_job_status(self, task_id, status):
        query = "UPDATE tasks SET status = ? WHERE id = ?"
        with get_db_connection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (status, task_id))
                connection.commit()
            except Exception as e:
                raise RuntimeError(f"Fel vid uppdatering av status: {e}")

    @staticmethod
    def sort_tasks(tasks):
        today = datetime.today().date()

        def sort_key(task):
            next_date = datetime.strptime(task.next_occurrence_date, '%Y-%m-%d').date()
            if next_date < today:
                return 0, next_date  # Försenade uppdrag först
            elif next_date == today:
                return 1, next_date  # Uppdrag för idag därefter
            else:
                return 2, next_date  # Framtida uppdrag sist

        return sorted(tasks, key=sort_key)
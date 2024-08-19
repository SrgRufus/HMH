# database.managers.assignment_manager.py
from black import datetime
from database.managers.assignment_fetcher import AssignmentFetcher
from database.connection import get_db_connection
from handlers.central_event_handler import event_handler

class AssignmentManager:
    def __init__(self, db_path: str, event_manager) -> None:
        self.db_path = db_path
        self.event_manager = event_manager
        self.fetcher = AssignmentFetcher(self.db_path)  # Kontrollera att denna attribut är korrekt instanserad

    def create_assignment(self, kommun, adress, ort, material, tomningsfrekvens, info, chauffor, koordinater, next_occurrence_date):
        query = """
            INSERT INTO assignments (kommun, adress, 
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
                event_handler.trigger_event('assignment_created', data)

            except Exception as e:
                raise RuntimeError(f"Fel vid skapande av uppdrag: {e}")

    def fetch_all_assignments(self):
        return self.fetcher.fetch_all_assignments()

    def delete_assignment(self, assignment_id):
        query = "DELETE FROM assignments WHERE id = ?"
        with get_db_connection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (assignment_id,))
                connection.commit()
            except Exception as e:
                raise RuntimeError(f"Fel vid borttagning av uppdrag: {e}")

    def fetch_assignment_by_id(self, assignment_id):
        query = "SELECT * FROM assignments WHERE id = ?"
        with get_db_connection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (assignment_id,))
                row = cursor.fetchone()
                if row:
                    return row
                else:
                    raise RuntimeError("Uppdraget kunde inte hittas.")
            except Exception as e:
                raise RuntimeError(f"Fel vid hämtning av uppdrag: {e}")

    def update_job_status(self, assignment_id, status):
        query = "UPDATE assignments SET status = ? WHERE id = ?"
        with get_db_connection(self.db_path) as connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, (status, assignment_id))
                connection.commit()
            except Exception as e:
                raise RuntimeError(f"Fel vid uppdatering av status: {e}")

    @staticmethod
    def sort_assignments(assignments):
        today = datetime.today().date()

        def sort_key(assignment):
            next_date = datetime.strptime(assignment.next_occurrence_date, '%Y-%m-%d').date()
            if next_date < today:
                return 0, next_date  # Försenade uppdrag först
            elif next_date == today:
                return 1, next_date  # Uppdrag för idag därefter
            else:
                return 2, next_date  # Framtida uppdrag sist

        return sorted(assignments, key=sort_key)
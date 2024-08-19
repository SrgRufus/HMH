# database.managers.recurrence_manager.py : Hanterar återkommande uppdrag.
from datetime import datetime, timedelta

from database.models import Assignment
from handlers.central_event_handler import event_handler


class RecurrenceManager:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    @staticmethod # Om den inte fungerar, ta bort staticmethod och addera self till argumentet utav funktionen
    def create_recurring_assignment(assignment, recurrence_interval_days, event_manager):
        """
        Skapar ett återkommande assignment baserat på ett befintligt assignment.
        :param assignment: Det befintliga uppdraget (assignment) att basera det nya på.
        :param recurrence_interval_days: Antal dagar mellan varje förekomst.
        :param event_manager: Instans av EventManager för att hantera uppdrag.
        :return: Det nya återkommande Assignment-objektet.
        """

        # Säkerställ att next_occurrence_date är ett datetime-objekt
        if isinstance(assignment.next_occurrence_date, str):
            assignment.next_occurrence_date = datetime.strptime(assignment.next_occurrence_date, '%Y-%m-%d')

        # Skapa nästa datum för det återkommande uppdraget
        next_date = assignment.next_occurrence_date + timedelta(days=recurrence_interval_days)

        # Skapa ett nytt Assignment-objekt baserat på det ursprungliga uppdraget
        new_assignment = Assignment(
            kommun=assignment.kommun,
            adress=assignment.adress,
            ort=assignment.ort,
            material=assignment.material,
            tomningsfrekvens=assignment.tomningsfrekvens,
            info=assignment.info,
            chauffor=assignment.chauffor,
            koordinater=assignment.koordinater,
            status=assignment.status,
            senast_hamtad=assignment.senast_hamtad,
            image_path=assignment.image_path,
            next_occurrence_date=next_date  # Detta är nu säkert ett datetime-objek
        )

        # Infoga det nya uppdraget i databasen och trigga event
        event_manager.insert_assignment(new_assignment)
        event_handler.trigger_event('assignment_created', new_assignment)

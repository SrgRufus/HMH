# database.managers.recurrence_manager.py : Hanterar återkommande uppdrag.
from datetime import datetime, timedelta

from database.models import Task
from handlers.central_event_handler import event_handler


class RecurrenceManager:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    @staticmethod # Om den inte fungerar, ta bort staticmethod och addera self till argumentet utav funktionen
    def create_recurring_task(task, recurrence_interval_days, event_manager):
        """
        Skapar ett återkommande task baserat på ett befintligt task.
        :param task: Det befintliga uppdraget (task) att basera det nya på.
        :param recurrence_interval_days: Antal dagar mellan varje förekomst.
        :param event_manager: Instans av EventManager för att hantera uppdrag.
        :return: Det nya återkommande Task-objektet.
        """

        # Säkerställ att next_occurrence_date är ett datetime-objekt
        if isinstance(task.next_occurrence_date, str):
            task.next_occurrence_date = datetime.strptime(task.next_occurrence_date, '%Y-%m-%d')

        # Skapa nästa datum för det återkommande uppdraget
        next_date = task.next_occurrence_date + timedelta(days=recurrence_interval_days)

        # Skapa ett nytt Task-objekt baserat på det ursprungliga uppdraget
        new_task = Task(
            kommun=task.kommun,
            adress=task.adress,
            ort=task.ort,
            material=task.material,
            tomningsfrekvens=task.tomningsfrekvens,
            info=task.info,
            chauffor=task.chauffor,
            koordinater=task.koordinater,
            status=task.status,
            senast_hamtad=task.senast_hamtad,
            image_path=task.image_path,
            next_occurrence_date=next_date  # Detta är nu säkert ett datetime-objekt
        )

        # Infoga det nya uppdraget i databasen och trigga event
        event_manager.insert_task(new_task)
        event_handler.trigger_event('task_created', new_task)

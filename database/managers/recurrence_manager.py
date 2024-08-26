# database/managers/recurrence_manager.py
from datetime import timedelta

from utils import validate_and_parse_date
from database import connection, models  # Importera connection och models modulerna

class RecurrenceManager:
    def __init__(self):
        """Konstruktor för RecurrenceManager som initierar en trådsäker session."""
        self.session = connection.scoped_session_instance()

    @staticmethod
    def calculate_recurring_task(task, recurrence_interval_days):
        """
        Beräknar nästa förekomst av en uppgift baserat på ett återkommande intervall.
        :param task: Den ursprungliga uppgiften.
        :param recurrence_interval_days: Antalet dagar mellan varje förekomst av uppgiften.
        :return: En ny Task-instans som representerar den återkommande uppgiften.
        """
        # Validera och parsa datumet för nästa förekomst av uppgiften
        task.next_occurrence_date = validate_and_parse_date(task.next_occurrence_date)
        # Beräkna nästa förekomstdatum baserat på det angivna intervallet
        next_date = task.next_occurrence_date + timedelta(days=recurrence_interval_days)
        # Skapa en ny uppgift med det beräknade nästa förekomstdatumet
        new_task = models.Task(
            kommun=task.kommun,
            adress=task.adress,
            ort=task.ort,
            material=task.material,
            tomningsfrekvens=task.tomningsfrekvens,
            info=task.info,
            chauffor=task.chauffor,
            koordinater=task.koordinater,
            next_occurrence_date=next_date
        )
        return new_task

    def create_and_add_recurring_task(self, task, recurrence_interval_days, event_manager):
        """
        Skapar och lägger till en återkommande uppgift i databasen och triggar en händelse.
        :param task: Den ursprungliga uppgiften.
        :param recurrence_interval_days: Antalet dagar mellan varje förekomst av uppgiften.
        :param event_manager: EventManager-instansen för att hantera händelser.
        """
        new_task = self.calculate_recurring_task(task, recurrence_interval_days)  # Beräkna och skapa den återkommande uppgiften
        event_manager.insert_task(new_task)  # Lägg till den nya uppgiften i databasen
        event_manager.event_handler.trigger_event('task_created', new_task)  # Trigga en händelse för att uppgiften skapats

    def close(self):
        """Stänger databassessionen."""
        self.session.close()

# database/managers/event_manager.py
import logging

from handlers import CentralEventHandler
from database import connection, models  # Importera connection och models modulerna


class EventManager:
    def __init__(self, recurrence_manager):
        """
        Konstruktor för EventManager som initierar nödvändiga komponenter för händelsehantering.
        :param recurrence_manager: Manager för att hantera återkommande uppgifter.
        """
        self.session = connection.scoped_session_instance()  # Skapa en trådsäker session
        self.recurrence_manager = recurrence_manager  # Spara en referens till RecurrenceManager
        self.event_handler = CentralEventHandler()  # Initiera en central händelsehanterare

    def setup_handlers(self):
        """Registrerar händelsehanterare för olika typer av händelser."""
        self.event_handler.register_handler('task_completed', self.handle_task_completed)

    def handle_task_completed(self, task: models.Task):
        """
        Hantera händelsen när en uppgift slutförs genom att skapa en återkommande uppgift.
        :param task: Uppgiften som just har slutförts.
        """
        try:
            self.recurrence_manager.create_recurring_task(task, recurrence_interval_days=7)  # Skapa en återkommande uppgift
        except Exception as e:
            logging.error(f"Error handling task completed event: {e}")  # Logga eventuella fel som inträffar

    def insert_task(self, task: models.Task):
        """
        Infoga en ny uppgift i databasen och trigga en 'task_created' händelse.
        :param task: Uppgiften som ska infogas i databasen.
        """
        self.session.add(task)  # Lägg till uppgiften i sessionen
        self.session.commit()  # Utför commit för att spara ändringarna
        try:
            self.event_handler.trigger_event('task_created', task)  # Trigga en händelse för att uppgiften skapats
        except Exception as e:
            logging.error(f"Error triggering task created event: {e}")  # Logga eventuella fel som inträffar

    def close(self):
        """Stänger databassessionen."""
        self.session.close()

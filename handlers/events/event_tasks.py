# handlers/events/event_tasks.py
import logging

class TaskCreatedEvent:
    @staticmethod
    def handle(data):
        """
        Hanterar logiken för när ett uppdrag skapas.
        """
        logging.info(f"Task created with data: {data}")
        # Logik för att hantera uppdraget
        pass

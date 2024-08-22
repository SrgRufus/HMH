# handlers.events.event_tasks.py

class TaskCreatedEvent:
    @staticmethod
    def handle(data):
        """
        Hanterar logiken för när ett uppdrag skapas.
        """
        print("Task created with data:", data)
        # Logik för att hantera uppdraget
        pass



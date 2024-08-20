# Root.main.py
import sys
from PyQt5.QtWidgets import QApplication
from config import DB_PATH
from database.db_manager import DBManager
from gui.mainwindow import MainWindow
from database.managers.event_manager import EventManager
from database.managers.recurrence_manager import RecurrenceManager
from database.managers.task_manager import TaskManager
from handlers.central_event_handler import event_handler


# Om du vill behålla testkoden, flytta den till en separat funktion
def test_function():
    def some_potentially_failing_function(ska_kasta_undantag):
        if ska_kasta_undantag:
            raise ValueError("Ett exempel på ett undantag")
        return "Funktionen kördes utan problem"

    try:
        result = some_potentially_failing_function(True)  # Här skickar vi True som argument
        print(result)
    except ValueError as e:
        print(f"Ett fel inträffade: {e}")

# Definiera en funktion som hanterar händelsen
def on_task_created(task_data):
    print(f"Task created: {task_data}")
    # Här kan du lägga logik för att uppdatera UI, logga eller något annat

# Registrera händelsehanteraren för 'task_created'
event_handler.register_handler('task_created', on_task_created)

# Den riktiga main-funktionen för att starta din applikation
def main():
    app = QApplication(sys.argv)

    # Initialiserar databas manager (DBManager)
    db_manager = DBManager(DB_PATH)
    db_manager.init_db()

    # Skapar RecurrenceManager, EventManager, TaskManager och MainWindow-klassen och kopplar ihop dem
    recurrence_manager = RecurrenceManager(DB_PATH)
    event_manager = EventManager(DB_PATH, recurrence_manager)
    task_manager = TaskManager(DB_PATH, event_manager)
    window = MainWindow(DB_PATH, event_manager, task_manager)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    # Om du vill köra testkoden, anropa den här:
    # test_function()

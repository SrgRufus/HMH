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

def initialize_database():
    """Initierar databasen och returnerar DBManager instansen"""
    db_manager = DBManager(DB_PATH)
    db_manager.init_db()
    return db_manager

def initialize_managers():
    """Initiera och returnera de "managers" som krävs för applikationen."""
    recurrence_manager = RecurrenceManager()
    event_manager = EventManager(recurrence_manager=recurrence_manager)
    task_manager = TaskManager()
    return recurrence_manager, event_manager, task_manager

def register_event_handlers():
    """Registrerar globala event hanterare för applikationen"""
    event_handler.register_handler('task_created', on_task_created)

def on_task_created(task_data):
    """Hanterar funktionen som kallas när ett uppdrag skapas"""
    print(f"Task created: {task_data}")

def main():
    app = QApplication(sys.argv)

    # Initiering databas och managers, typ
    initialize_database()
    initialize_managers()
    register_event_handlers()

    # Initiera och visa första sidan i applikationen
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    # Om du vill köra testkoden, anropa den här:
    # test_function()

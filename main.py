# Root.main.py
import sys
from PyQt5.QtWidgets import QApplication
from config import DB_PATH
from database.db_manager import DBManager
from gui.mainwindow import MainWindow
from database.managers.event_manager import EventManager
from database.managers.recurrence_manager import RecurrenceManager
from database.managers.assignment_manager import AssignmentManager
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
def on_assignment_created(assignment_data):
    print(f"Assignment created: {assignment_data}")
    # Här kan du lägga logik för att uppdatera UI, logga eller något annat

# Registrera händelsehanteraren för 'assignment_created'
event_handler.register_handler('assignment_created', on_assignment_created)

# Den riktiga main-funktionen för att starta din applikation
def main():
    app = QApplication(sys.argv)

    # Initialiserar databas manager (DBManager)
    db_manager = DBManager(DB_PATH)
    db_manager.init_db()

    # Skapar RecurrenceManager, EventManager, AssignmentManager och MainWindow-klassen och kopplar ihop dem
    recurrence_manager = RecurrenceManager(DB_PATH)
    event_manager = EventManager(DB_PATH, recurrence_manager)
    assignment_manager = AssignmentManager(DB_PATH, event_manager)
    window = MainWindow(DB_PATH, event_manager, assignment_manager)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    # Om du vill köra testkoden, anropa den här:
    # test_function()

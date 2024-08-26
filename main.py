# main.py
import sys
import logging
from PyQt5.QtWidgets import QApplication
from config import DB_PATH
from database import DBManager, EventManager, RecurrenceManager, TaskManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gui import MainWindow
from handlers import event_handler

logging.basicConfig(level=logging.INFO)


def initialize_database():
    """Initierar databasen och returnerar DBManager instansen samt en SQLAlchemy-session"""
    try:
        db_manager = DBManager(DB_PATH)
        db_manager.init_db()

        # Skapa en SQLAlchemy engine
        engine = create_engine(f'sqlite:///{DB_PATH}')

        # Skapa en sessionmaker och en session
        session_maker = sessionmaker(bind=engine)
        session = session_maker()

        logging.info("Database initialized successfully.")
        return db_manager, session
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        sys.exit(1)


def initialize_managers(session):
    """Initiera och returnera de 'managers' som krävs för applikationen."""
    try:
        recurrence_manager = RecurrenceManager()
        event_manager = EventManager(recurrence_manager=recurrence_manager)
        task_manager = TaskManager(session)  # Skicka in sessionen här
        logging.info("Managers initialized successfully.")
        return recurrence_manager, event_manager, task_manager
    except Exception as e:
        logging.error(f"Error initializing managers: {e}")
        sys.exit(1)


def register_event_handlers():
    """Registrerar globala event hanterare för applikationen"""
    event_handler.register_handler('task_created', on_task_created)
    logging.info("Event handlers registered successfully.")


def on_task_created(task_data):
    """Hanterar funktionen som kallas när ett uppdrag skapas"""
    logging.info(f"Task created: {task_data}")


def main():
    app = QApplication(sys.argv)

    # Initiering databas och managers
    db_manager, session = initialize_database()
    initialize_managers(session)
    register_event_handlers()

    # Initiera och visa första sidan i applikationen
    window = MainWindow(session)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

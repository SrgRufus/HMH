# database.queries.task_queries.py
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database.models import Task
from database.connection import engine


Session = sessionmaker(bind=engine)
session = Session()


def get_tasks_by_date(date):
    """
    Hämta uppdrag baserat på ett datum.
    Validera för att försäkra mig om att det är ett datetime objekt
    """
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format: {date}. Expected format is YYYY-MM-DD.")

    if not isinstance(date, datetime):
        raise ValueError(
            "The 'date' parameter must be a datetime object or a valid date string in 'YYYY-MM-DD' format.")

    return session.query(Task).filter(Task.next_occurrence_date == date).all()


def get_all_tasks():
    """Hämta alla uppdrag."""
    return session.query(Task).all()


# ORM-based replacements for raw SQL queries:
def create_task(task_data):
    """Mata in ett nytt uppdrag i databasen."""
    new_task = Task(**task_data)
    session.add(new_task)
    session.commit()


def update_task_status(task_id, status, image_path=None):
    """Uppdatera status för ett uppdrag."""
    task = session.query(Task).get(task_id)
    if task:
        task.status = status
        if image_path:
            task.image_path = image_path
        session.commit()
    else:
        raise ValueError(f"Task with ID {task_id} not found.")


def delete_task(task_id):
    """Radera ett uppdrag med dens ID."""
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
    else:
        raise ValueError(f"Task with ID {task_id} not found.")

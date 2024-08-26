# database/managers/task_manager.py
import logging
from datetime import datetime
from typing import Optional

from utils import calculate_next_date
from .. import TaskHistory, Task


class TaskManager:
    def __init__(self, session):
        """Konstruktor för TaskManager som tar en databas-sessions som parameter."""
        self.session = session

    def create_task(self, task_data: dict) -> bool:
        """
        Skapar en ny uppgift baserat på en data-dictionary.
        :param task_data: Dictionary med data för att skapa en ny uppgift.
        :return: True om uppgiften skapades framgångsrikt, annars False.
        """
        try:
            new_task = Task(
                kommun=task_data.get('kommun'),
                adress=task_data.get('adress'),
                ort=task_data.get('ort'),
                material=task_data.get('material'),
                tomningsfrekvens=task_data.get('tomningsfrekvens'),
                info=task_data.get('info', ''),
                chauffor=task_data.get('chauffor', ''),
                koordinater=task_data.get('koordinater', ''),
                next_occurrence_date=task_data.get('next_occurrence_date'),
                status=task_data.get('status', 'Aktiv')  # Standardstatus är "Aktiv" om inget annat anges
            )
            with self.session as session:
                session.add(new_task)  # Lägg till den nya uppgiften i sessionen
                session.commit()  # Utför commit för att spara ändringarna
            logging.info("Successfully created a new task.")  # Logga framgången
            return True
        except Exception as e:
            logging.error(f"Error creating new task: {e}")  # Logga eventuella fel som inträffar
            self.session.rollback()  # Rollbacka sessionen om ett fel uppstår
            return False

    def get_tasks_by_status(self, status: str) -> list:
        """
        Hämtar uppgifter baserat på deras status.
        :param status: Status att filtrera uppgifterna på.
        :return: En lista av uppgifter med den angivna statusen.
        """
        try:
            with self.session as session:
                tasks = session.query(Task).filter(Task.status == status).all()
                return tasks
        except Exception as e:
            logging.error(f"Error fetching tasks by status {status}: {e}")  # Logga eventuella fel som inträffar
            return []

    def update_task_status(self, task_id: int, updated_data: dict) -> bool:
        """
        Uppdaterar en uppgift med de angivna data.
        :param task_id: ID för uppgiften som ska uppdateras.
        :param updated_data: Dictionary med uppdaterad data för uppgiften.
        :return: True om uppdateringen lyckades, annars False.
        """
        try:
            with self.session as session:
                task = session.query(Task).get(task_id)  # Hämta uppgiften baserat på ID
                if not task:
                    logging.warning(f"Task with ID {task_id} not found")  # Logga en varning om uppgiften inte hittas
                    return False

                # Uppdatera uppgiften med den nya data
                for key, value in updated_data.items():
                    setattr(task, key, value)

                session.commit()  # Utför commit för att spara ändringarna
                logging.info(f"Task {task_id} updated successfully.")  # Logga framgången
                return True
        except Exception as e:
            logging.error(f"Error updating task: {e}")  # Logga eventuella fel som inträffar
            session.rollback()  # Rollbacka sessionen om ett fel uppstår
            return False

    def get_tasks_by_date(self, start_date, end_date):
        """
        Hämtar uppgifter mellan två datum.
        :param start_date: Startdatum för intervallet.
        :param end_date: Slutdatum för intervallet.
        :return: En lista av uppgifter inom det angivna datumintervallet.
        """
        try:
            with self.session as session:
                tasks = session.query(Task).filter(
                    Task.next_occurrence_date >= start_date,
                    Task.next_occurrence_date <= end_date
                ).all()
            return tasks
        except Exception as e:
            logging.error(f"Error fetching tasks: {e}")  # Logga eventuella fel som inträffar
            return []

    def get_all_tasks(self):
        """
        Hämtar alla uppgifter från databasen.
        :return: En lista av alla uppgifter.
        """
        with self.session as session:
            tasks = session.query(Task).all()
            return tasks

    @staticmethod
    def sort_tasks(tasks: list) -> list:
        """
        Sorterar uppgifter efter deras nästa förekomstdatum.
        :param tasks: Listan av uppgifter som ska sorteras.
        :return: En sorterad lista av uppgifter.
        """
        try:
            return sorted(tasks, key=lambda task: task.next_occurrence_date)
        except Exception as e:
            logging.error(f"Error sorting tasks: {e}")  # Logga eventuella fel som inträffar
            return tasks

    def delete_task(self, task_id: int) -> None:
        """
        Tar bort en uppgift baserat på dess ID.
        :param task_id: ID för uppgiften som ska tas bort.
        """
        try:
            with self.session as session:
                task = session.query(Task).get(task_id)
                if task:
                    session.delete(task)  # Ta bort uppgiften från sessionen
                    session.commit()  # Utför commit för att spara ändringarna
                else:
                    raise ValueError(f"Task with ID {task_id} not found.")  # Kasta ett fel om uppgiften inte hittas
        except Exception as e:
            logging.error(f"Error deleting task: {e}")  # Logga eventuella fel som inträffar
            self.session.rollback()  # Rollbacka sessionen om ett fel uppstår
            raise RuntimeError("An error occurred while deleting the task.")  # Kasta ett RuntimeError

    def fetch_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Hämtar en uppgift baserat på dess ID.
        :param task_id: ID för uppgiften som ska hämtas.
        :return: Uppgiften om den hittas, annars None.
        """
        try:
            with self.session as session:
                task = session.query(Task).get(task_id)
                return task
        except Exception as e:
            logging.error(f"Error fetching task with ID {task_id}: {e}")  # Logga eventuella fel som inträffar
            return None

    def complete_task_and_create_new(self, task_id: int) -> Optional[Task]:
        """
        Slutför en uppgift, spara historik, och skapa en ny uppgift med nästa förekomstdatum.
        :param task_id: ID för uppgiften som ska slutföras.
        :return: Den nya uppgiften om allt går bra, annars None.
        """
        try:
            with self.session as session:
                task = session.query(Task).get(task_id)
                if not task:
                    logging.warning(f"Task with ID {task_id} not found")  # Logga en varning om uppgiften inte hittas
                    return None

                # Spara den nuvarande uppgiftens detaljer i historiken
                history = TaskHistory(
                    task_id=task.id,
                    kommun=task.kommun,
                    adress=task.adress,
                    ort=task.ort,
                    material=task.material,
                    tomningsfrekvens=task.tomningsfrekvens,
                    info=task.info,
                    chauffor=task.chauffor,
                    koordinater=task.koordinater,
                    status=task.status,
                    completion_date=datetime.now()
                )
                session.add(history)  # Lägg till historikposten i sessionen

                # Markera den nuvarande uppgiften som slutförd
                task.status = 'Completed'
                session.commit()  # Utför commit för att spara ändringarna

                # Beräkna nästa förekomstdatum
                next_occurrence_date = calculate_next_date(task.tomningsfrekvens, datetime.now())

                # Skapa en ny uppgift med nästa förekomstdatum
                new_task = Task(
                    kommun=task.kommun,
                    adress=task.adress,
                    ort=task.ort,
                    material=task.material,
                    tomningsfrekvens=task.tomningsfrekvens,
                    info=task.info,
                    chauffor=task.chauffor,
                    koordinater=task.koordinater,
                    next_occurrence_date=next_occurrence_date,
                    status='Aktiv'
                )
                session.add(new_task)  # Lägg till den nya uppgiften i sessionen
                session.commit()  # Utför commit för att spara ändringarna

                logging.info(f"Task {task_id} completed and new task created with ID {new_task.id}")  # Logga framgången
                return new_task
        except Exception as e:
            logging.error(f"Error completing task and creating new task: {e}")  # Logga eventuella fel som inträffar
            session.rollback()  # Rollbacka sessionen om ett fel uppstår
            return None

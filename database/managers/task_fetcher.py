# database/managers/task_fetcher.py
from functools import lru_cache

from database import connection, models


class TaskFetcher:
    def __init__(self):
        """Konstruktor för TaskFetcher som initierar en trådsäker session."""
        self.session = connection.scoped_session_instance()

    def fetch_all_tasks(self, page_num=1, page_size=20):
        """
        Hämtar alla uppgifter med pagineringsstöd.
        :param page_num: Sidnummer för pagineringen (standard är 1).
        :param page_size: Antal uppgifter per sida (standard är 20).
        :return: En lista av uppgifter för den angivna sidan.
        """
        return self.session.query(models.Task).limit(page_size).offset((page_num - 1) * page_size).all()

    @lru_cache(maxsize=128)
    def fetch_tasks_sorted_by_date(self):
        """
        Hämtar uppgifter sorterade efter nästa förekomstdatum, med caching.
        :return: En lista av sorterade uppgifter.
        """
        return self.session.query(models.Task).order_by(models.Task.next_occurrence_date.asc()).all()

    def fetch_tasks_for_current_week(self, start_of_week, end_of_week):
        """
        Hämtar uppgifter som ska utföras under den aktuella veckan.
        :param start_of_week: Startdatum för veckan.
        :param end_of_week: Slutdatum för veckan.
        :return: En lista av uppgifter för den aktuella veckan.
        """
        return self.session.query(models.Task).filter(models.Task.next_occurrence_date.between(start_of_week, end_of_week)).all()

    def fetch_task_by_id(self, task_id):
        """
        Hämtar en uppgift baserat på dess ID.
        :param task_id: ID för uppgiften som ska hämtas.
        :return: Uppgiften om den hittas, annars None.
        """
        return self.session.query(models.Task).get(task_id)

    def close(self):
        """Stänger databassessionen."""
        self.session.close()

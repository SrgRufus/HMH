# database.db_manager.py : Grundläggande databasoperationer.
from config import DB_PATH
from database.connection import get_db_connection
from database.operations import execute_query
from database.queries.task_queries import CREATE_TASKS_TABLE


# Hanterar grundläggande databasoperationer som initiering av databasen.
class DBManager:

    # Initierar en ny instans av DBManager med angiven databasväg
    def __init__(self, db_path=DB_PATH):
        """
        :param db_path: Sökvägen till databasfilen.
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    # Initierar databasen genom att skapa nödvändiga tabeller.
    def init_db(self):
        execute_query(self.db_path, CREATE_TASKS_TABLE)

    # Hämtar alla rader för en given query.
    def fetch_all(self, query):
        """
        :param query: SQL-frågan som ska exekveras.
        :return: Lista av tuples med resultatet av frågan.
        """
        print(f'Opening connection to {self.db_path}')
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        print('Connection closed')
        return rows

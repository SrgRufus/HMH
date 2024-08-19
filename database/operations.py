# database.operations.py
import logging
import sqlite3

from database.connection import get_db_connection

# Konfigurera loggning
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Exekverar en SQL-fråga med felhantering.
def execute_query(db_path, query, parameters=()):
    """
    :param db_path: Sökväg till databasen.
    :param query: SQL-frågan som ska köras.
    :param parameters: Parametrar att binda till SQL-frågan.
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
            logging.info(f"Successfully executed query: {query} with parameters: {parameters}")
            return cursor  # Returnera cursor för vidare användning
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        raise
    except Exception as e:
        logging.error(f"General error: {e}")
        raise


# Exekverar en SELECT-fråga och hämtar alla rader.
def fetch_all(db_path, query, parameters=()):
    """
    :param db_path: Sökväg till databasen.
    :param query: SQL-frågan som ska köras.
    :param parameters: Parametrar att binda till SQL-frågan.
    :return: Resultatuppsättningen som en lista av tuples.
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            rows = cursor.fetchall()
            logging.info(f"Successfully fetched data with query: {query} and parameters: {parameters}")
            return rows
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        raise
    except Exception as e:
        logging.error(f"General error: {e}")
        raise

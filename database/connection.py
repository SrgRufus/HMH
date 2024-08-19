# database.connection.py
import logging
import sqlite3
from contextlib import contextmanager

from config import DB_PATH

# Konfigurera loggning
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Hanterar anslutning till SQLite-databasen med kontext manager.
@contextmanager
def get_db_connection(db_path=DB_PATH):
    """
    :param db_path: Sökväg till databasfilen.
    """
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    except sqlite3.DatabaseError as e:
        logging.error(f"Database error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    finally:
        conn.close()
        logging.info(f"Connection to {db_path} closed")

# database/operations.py
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .connection import Session

# Konfigurera grundläggande logging för att logga händelser i systemet
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_query(query_func, *args, **kwargs):
    """
    Utför en databasfråga med korrekt felhantering.
    :param query_func: Funktionen som ska utföra själva frågan.
    :param args: Argument som ska skickas till query_func.
    :param kwargs: Nyckelordargument som ska skickas till query_func.
    :return: Resultatet av frågan om lyckad, annars höjs ett undantag.
    """
    session = Session()  # Skapa en ny session
    try:
        result = query_func(session, *args, **kwargs)  # Kör frågan med de givna argumenten
        session.commit()  # Utför commit om allt går bra
        logging.info(f"Successfully executed query with parameters: {args}, {kwargs}")  # Logga framgången
        return result  # Returnera resultatet av frågan
    except IntegrityError as e:
        logging.error(f"Integrity error: {e}")  # Logga fel relaterade till databasintegritet
        session.rollback()  # Rollbacka sessionen
        raise  # Kasta om felet
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")  # Logga andra SQLAlchemy-relaterade fel
        session.rollback()  # Rollbacka sessionen
        raise  # Kasta om felet
    finally:
        session.close()  # Stäng sessionen i alla fall

def batch_insert(model_class, data_list):
    """
    Utför en batch-insert av flera poster till databasen.
    :param model_class: Modellen/Tabellen som posterna ska infogas i.
    :param data_list: En lista av dictionarys som representerar posterna som ska infogas.
    """
    session = Session()  # Skapa en ny session
    try:
        session.bulk_insert_mappings(model_class, data_list)  # Utför en batch-insert
        session.commit()  # Utför commit om allt går bra
        logging.info(f"Batch insert successful for {len(data_list)} records.")  # Logga framgången
    except SQLAlchemyError as e:
        logging.error(f"Batch insert error: {e}")  # Logga SQLAlchemy-relaterade fel
        session.rollback()  # Rollbacka sessionen
        raise  # Kasta om felet
    finally:
        session.close()  # Stäng sessionen i alla fall

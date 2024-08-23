# database.operations.py : Adding batch operations and enhanced error handling
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database.connection import engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Session = sessionmaker(bind=engine)

def execute_query(query_func, *args, **kwargs):
    """Execute a query with proper error handling."""
    session = Session()
    try:
        result = query_func(session, *args, **kwargs)
        session.commit()
        logging.info(f"Successfully executed query with parameters: {args}, {kwargs}")
        return result
    except IntegrityError as e:
        logging.error(f"Integrity error: {e}")
        session.rollback()
        raise
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def batch_insert(model_class, data_list):
    """Insert multiple records in a batch."""
    session = Session()
    try:
        session.bulk_insert_mappings(model_class, data_list)
        session.commit()
        logging.info(f"Batch insert successful for {len(data_list)} records.")
    except SQLAlchemyError as e:
        logging.error(f"Batch insert error: {e}")
        session.rollback()
        raise
    finally:
        session.close()


# def fetch_all(query_func, *args, **kwargs):
#     session = Session()
#     try:
#         return query_func(session, *args, **kwargs)
#     except SQLAlchemyError as e:
#         logging.error(f"Database error: {e}")
#         raise
#     finally:
#         session.close()


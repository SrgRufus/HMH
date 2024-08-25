# database/connection.py
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DB_PATH

# Ensure DB_PATH is correctly formatted and create an engine
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Initialize the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class using sessionmaker
Session = sessionmaker(bind=engine)  # This is the session factory

# Use a scoped_session for thread safety, passing the Session factory
scoped_session_instance = scoped_session(Session)  # Thread-safe session

# Define the get_db_connection function
@contextmanager
def get_db_connection():
    """Provide a transactional scope around a series of operations."""
    session = scoped_session_instance()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"An error occurred: {e}")
        raise
    finally:
        session.close()

def init_db():
    """Initialize the database and create all tables."""
    from .models import Base
    Base.metadata.create_all(bind=engine)

# database.connection.py
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DB_PATH
from database.models import Base

# Se till att DB_PATH är korrekt formaterad och skapa en motor
DATABASE_URL = f"sqlite:///{DB_PATH}"  # Länkar till din befintliga SQLite-databas

# Initierar databasmotorn med formatet DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)

# Skapa en konfigurerad "Session" klass
Session = sessionmaker(bind=engine)

# Egentligen valfritt: Använd en scoped_session (för tråd-säkerhet):
scoped_session_instance = scoped_session(Session)

# Konfigurera loggning
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_db():
    """
    Initiera databasen och skapa alla tabeller.
    """

    Base.metadata.create_all(bind=engine)
    logging.info("Database initialized and tables created.")

# Context manager för att överse databas sessioner
@contextmanager
def get_db_connection():
    """
    Provide a transactional scope around a series of operations.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:  # Fånga upp SQLAlchemy-specifika "errors"
        session.rollback()
        logging.error(f"SQLAlchemy error occurred: {e}")
        raise
    except Exception as e:  # Fånga upp alla andra
        session.rollback()
        logging.error(f"Unexpected error occurred: {e}")
        raise
    finally:
        session.close()

# database/db_manager.py
from config import DB_PATH
from contextlib import contextmanager
from .models import Base
from .connection import create_engine, Session


class DBManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=True, pool_size=10, max_overflow=20)
        self.Session = Session(bind=self.engine)


    def init_db(self):
        """Initierar databasen och skapar alla tabeller"""
        Base.metadata.create_all(self.engine)


    @contextmanager
    def get_session(self):
        """Context manager för sessions hantering."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Error during session: {e}")
        finally:
            session.close()


    def close(self):
        """Stäng databas anslutningen"""
        self.engine.dispose()

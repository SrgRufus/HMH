# database/db_manager.py
from config import DB_PATH
from contextlib import contextmanager
from database.models import Base
from database.connection import create_engine, Session

class DBManager:
    def __init__(self, db_path=DB_PATH):
        """
        Konstruktor för DBManager som initierar databasmotorn och session-fabriken.
        :param db_path: Sökvägen till databasen (default är DB_PATH från config).
        """
        self.db_path = db_path  # Lagra databasens sökväg
        self.engine = create_engine(f'sqlite:///{db_path}', echo=True, pool_size=10, max_overflow=20)
        # Skapa en SQLAlchemy-motor för att hantera databasanslutningar med en anslutningspool
        self.Session = Session(bind=self.engine)  # Skapa en session fabriksmetod bunden till denna motor

    def init_db(self):
        """Initierar databasen och skapar alla tabeller baserat på modellernas metadata."""
        Base.metadata.create_all(self.engine)  # Skapa alla tabeller i databasen

    @contextmanager
    def get_session(self):
        """
        Kontexthanterare för att hantera databas-sessions.
        Säkerställer att sessions committas eller rollbacks beroende på om ett fel inträffar.
        """
        session = self.Session()  # Skapa en ny session
        try:
            yield session  # Returnera sessionen till anroparen
            session.commit()  # Utför commit om inga fel inträffar
        except Exception as e:
            session.rollback()  # Återställ sessionen om ett fel uppstår
            raise RuntimeError(f"Error during session: {e}")  # Kasta ett nytt felmeddelande
        finally:
            session.close()  # Stäng sessionen

    def close(self):
        """Stänger alla aktiva databasanslutningar."""
        self.engine.dispose()  # Avslutar alla öppna anslutningar


# database/connection.py
import logging  # Importera logging-modulen för att logga fel och information
from contextlib import contextmanager  # Importera contextmanager för att skapa kontexthanterare

from sqlalchemy import create_engine  # Importera create_engine för att skapa databasmotorn
from sqlalchemy.orm import scoped_session, \
    sessionmaker  # Importera scoped_session och sessionmaker för att hantera databassessioner

from config import DB_PATH  # Importera DB_PATH från config-filen för att få sökvägen till databasen

# Skapa en databas-URL genom att använda DB_PATH
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Initiera databasmotorn med den skapade URL:en
engine = create_engine(DATABASE_URL, echo=True)  # echo=True för att logga alla SQL-uttalanden

# Skapa en "Session" klasskonfiguration med sessionmaker, bunden till motorn
Session = sessionmaker(bind=engine)

# Använd scoped_session för trådsäker hantering av sessions, särskilt användbart i webapplikationer
scoped_session_instance = scoped_session(Session)

@contextmanager
def get_db_connection():
    """
    Kontexthanterare för att skapa och stänga databassessioner på ett säkert sätt.
    Hanterar commits och rollbacks automatiskt.
    """
    session = scoped_session_instance()  # Skapa en ny session
    try:
        yield session  # Ge sessionen till den kod som använder denna kontext
        session.commit()  # Utför commit om inga fel inträffar
    except Exception as e:
        session.rollback()  # Återställ sessionen om ett fel uppstår
        logging.error(f"An error occurred: {e}")  # Logga felet
        raise  # Kasta vidare felet så att det kan hanteras högre upp
    finally:
        session.close()  # Stäng sessionen

def init_db():
    """
    Initiera databasen genom att skapa alla definierade tabeller.
    Denna funktion används vanligtvis vid start av applikationen.
    """
    from .models import Base  # Importera Base-klassen från models för att kunna skapa tabeller
    Base.metadata.create_all(bind=engine)  # Skapa alla tabeller i databasen baserat på modellerna

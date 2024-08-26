# database.models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Skapa en basklass för alla modeller genom att anropa declarative_base
Base = declarative_base()

class Task(Base):
    """
    En SQLAlchemy-modell som representerar en uppgift i tasks-tabellen.
    Denna modell innehåller alla fält som behövs för att beskriva en uppgift.
    """
    __tablename__ = 'tasks'  # Ange tabellnamnet i databasen

    id = Column(Integer, primary_key=True)  # Unikt ID för varje uppgift
    kommun = Column(String)  # Kommunen där uppgiften är relevant
    adress = Column(String)  # Adressen för uppgiften
    ort = Column(String)  # Orten där uppgiften är placerad
    material = Column(String)  # Material som är relevant för uppgiften
    tomningsfrekvens = Column(String)  # Frekvens för tömning eller utförande av uppgiften
    info = Column(String)  # Ytterligare information om uppgiften
    chauffor = Column(String)  # Chauffören som utför uppgiften
    koordinater = Column(String)  # Geografiska koordinater för uppgiften
    status = Column(String, default='Aktiv')  # Status för uppgiften, med standardvärde "Aktiv"
    next_occurrence_date = Column(DateTime)  # Datum för nästa förekomst av uppgiften
    history = relationship("TaskHistory", back_populates="original_task")  # Relation till TaskHistory-modellen, som skapar kopplingar till historiken för denna uppgift


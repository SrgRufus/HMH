# database/history_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class TaskHistory(Base):
    """
    En SQLAlchemy-modell för att lagra historik av uppgifter i task_history-tabellen.
    Varje historikpost är kopplad till en specifik uppgift i tasks-tabellen.
    """
    __tablename__ = 'task_history'  # Ange tabellnamnet i databasen

    id = Column(Integer, primary_key=True)  # Unikt ID för varje historikpost
    task_id = Column(Integer, ForeignKey('tasks.id'))  # Referens till uppgiftens ID i tasks-tabellen
    kommun = Column(String)  # Kommunen där uppgiften är relevant
    adress = Column(String)  # Adressen för uppgiften
    ort = Column(String)  # Orten där uppgiften är placerad
    material = Column(String)  # Material som är relevant för uppgiften
    tomningsfrekvens = Column(String)  # Frekvens för tömning eller utförande av uppgiften
    info = Column(String)  # Ytterligare information om uppgiften
    chauffor = Column(String)  # Chauffören som utför uppgiften
    koordinater = Column(String)  # Geografiska koordinater för uppgiften
    status = Column(String)  # Status för uppgiften när historikposten skapades
    completion_date = Column(DateTime)  # Datum och tid då uppgiften slutfördes
    original_task = relationship("Task", back_populates="history")  # Relation till Task-modellen, vilket skapar en koppling till originaluppgiften
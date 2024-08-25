# database.models.py
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    """
    Representerar ett uppdrag (Task) i systemet.
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    kommun = Column(String(100), nullable=False)
    adress = Column(String(150), nullable=False)
    ort = Column(String(100), nullable=False)
    material = Column(String(50), nullable=False)
    tomningsfrekvens = Column(String(50), nullable=False)
    info = Column(String, default='')
    chauffor = Column(String, default='Unknown')
    koordinater = Column(String, default='0,0')
    next_occurrence_date = Column(DateTime, nullable=False)
    __table_args__ = (
        Index('ix_task_next_occurrence_date', 'next_occurrence_date'),
    )

    def __repr__(self):
        return f"<Task(id={self.id}, kommun={self.kommun}, adress={self.adress}, ort={self.ort})>"

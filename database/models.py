# database.models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# Representerar ett uppdrag (Assignment) i systemet.
@dataclass
class Assignment:
    id: Optional[int] = None  # ID genereras av databasen när det skapas
    kommun: str = ""
    adress: str = ""
    ort: str = ""
    material: str = ""
    tomningsfrekvens: str = ""
    info: Optional[str] = None
    chauffor: Optional[str] = None
    koordinater: Optional[str] = None
    status: str = 'Pending'
    senast_hamtad: Optional[str] = None
    image_path: Optional[str] = None
    next_occurrence_date: Optional[datetime] = field(default_factory=datetime.now)

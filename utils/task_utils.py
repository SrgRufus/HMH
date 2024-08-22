# utils.task_utils.py
from datetime import datetime
from utils.recurrence_utils import recurrence_mapping


def validate_task_data(tomningsfrekvens):
    """
    Validera de data som krävs för att skapa ett uppdrag.
    :param tomningsfrekvens: Frekvens för tömning.
    """
    validate_recurring_frequency(tomningsfrekvens)


def validate_recurring_frequency(tomningsfrekvens):
    if tomningsfrekvens not in recurrence_mapping:
        raise ValueError(f"Ogiltig tomningsfrekvens: {tomningsfrekvens}")


def calculate_next_occurrence(tomningsfrekvens, current_date):
    """
    Beräkna nästa datum för tömning baserat på frekvensen.
    :param tomningsfrekvens: Frekvens för tömning.
    :param current_date: Aktuellt datum.
    :return: Nästa datum som en datetime.
    """
    if not isinstance(current_date, datetime):
        raise ValueError("current_date måste vara ett datetime-objekt")
    return recurrence_mapping[tomningsfrekvens](current_date)



# utils.assignment_utils.py
from utils.recurrence_utils import recurrence_mapping
from utils.recurrence_utils import calculate_next_date


def validate_assignment_data(tomningsfrekvens):
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
    return calculate_next_date(tomningsfrekvens, current_date)

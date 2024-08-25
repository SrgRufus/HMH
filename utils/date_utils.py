# utils.date_utils.py
from datetime import datetime

def validate_and_parse_date(date_str):
    """
    Validerar och konverterar en datumsträng till ett datetime-objekt.
    :param date_str: Datum som sträng.
    :return: Ett datetime-objekt.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Ogiltigt datumformat: {date_str}. Förväntat format är YYYY-MM-DD.")

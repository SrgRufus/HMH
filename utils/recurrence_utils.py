# utils.recurring_dates.py : Beräkningar för återkommande datum.
import calendar
from datetime import datetime, timedelta


def next_day_of_week(current_date, target_weekday):
    days_ahead = target_weekday - current_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return current_date + timedelta(days=days_ahead)

# Nästa Måndag
def next_monday(current_date):
    return next_day_of_week(current_date, 0)

# Nästa Tisdag
def next_tuesday(current_date):
    return next_day_of_week(current_date, 1)

# Nästa Onsdag
def next_wednesday(current_date):
    return next_day_of_week(current_date, 2)

# Nästa Torsdag
def next_thursday(current_date):
    return next_day_of_week(current_date, 3)

# Nästa Fredag
def next_friday(current_date):
    return next_day_of_week(current_date, 4)

# Nästa Lördag
def next_saturday(current_date):
    return next_day_of_week(current_date, 5)

# Nästa Söndag
def next_sunday(current_date):
    return next_day_of_week(current_date, 6)

# Varje vecka, valfri dag.
def next_valfri(current_date):
    return current_date + timedelta(weeks=1)

# Två gånger i veckan, antar 3.5 dagar isär.
def next_twin_dates(current_date):
    return current_date + timedelta(days=3.5)

# Varannan vecka på jämna veckor
def next_even_week(current_date):
    week_num = current_date.isocalendar()[1]
    if week_num % 2 == 0:
        return current_date + timedelta(weeks=2)
    return current_date + timedelta(weeks=1)

# Varannan vecka på ojämna veckor
def next_odd_week(current_date):
    week_num = current_date.isocalendar()[1]
    if week_num % 2 != 0:
        return current_date + timedelta(weeks=2)
    return current_date + timedelta(weeks=1)

# Varje X veckor.
def next_every_x_weeks(current_date, x):
    return current_date + timedelta(weeks=x)

# Den första Torsdagen av nästa månad
def next_first_thursday(current_date):
    next_month = current_date.month % 12 + 1
    year = current_date.year + (current_date.month // 12)
    first_day = datetime(year, next_month, 1)
    return next_day_of_week(first_day, calendar.THURSDAY)

# Den 25:e av den här eller nästa månad
def next_25th_day(current_date):
    if current_date.day > 25:
        next_month = current_date.month % 12 + 1
        year = current_date.year + (current_date.month // 12)
    else:
        next_month = current_date.month
        year = current_date.year
    return datetime(year, next_month, 25)


# Kartläggningsfunktion
recurrence_mapping = {
    "Måndag, Varje vecka": next_monday,
    "Tisdag, Varje vecka": next_tuesday,
    "Onsdag, Varje vecka": next_wednesday,
    "Torsdag, Varje vecka": next_thursday,
    "Fredag, Varje vecka": next_friday,
    "Lördag, Varje vecka": next_saturday,
    "Söndag, Varje vecka": next_sunday,
    "Varje vecka (valfri dag)": next_valfri,
    "Två tillfällen varje vecka": next_twin_dates,
    "Jämn vecka": next_even_week,
    "Ojämn vecka": next_odd_week,
    "Var 4:e vecka, En gång i Månaden": lambda date: next_every_x_weeks(date, 4),
    "Var 6:e vecka": lambda date: next_every_x_weeks(date, 6),
    "Var 12:e vecka": lambda date: next_every_x_weeks(date, 12),
    "Den första Torsdagen i Månaden": next_first_thursday,
    "Den 25:e varje månad": next_25th_day
}

# Räkna ut nästa tömningsdatum baserat på tömningsfrekvens.
def calculate_next_date(frequency: str, current_date: datetime) -> datetime:
    """
    Beräknar nästa datum baserat på tömningsfrekvensen.
    :param frequency: Frekvensen (ex. "Varje vecka", "Jämn vecka")
    :param current_date: Nuvarande datum och tid
    :return: Nästa datum som datetime-objekt
    """
    if frequency not in recurrence_mapping:
        raise ValueError(f"Frekvensen stöds inte: {frequency}")

    # Använd den matchande funktionen från recurrence_mapping
    return recurrence_mapping[frequency](current_date)

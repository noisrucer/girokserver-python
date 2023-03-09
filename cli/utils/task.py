from datetime import datetime, timedelta
from calendar import monthrange

def is_valid_year(year: int):
    if year < datetime.now().year - 3 or year > datetime.now().year + 10:
        return False
    return True
    
    
def is_valid_month(month: int):
    if month <= 0 or month > 12:
        return False
    return True


def is_valid_day(year: int, month: int, day: int):
    if day not in range(1, monthrange(year, month)[1]):
        return False
    return True


def is_valid_hour(hour: int):
    if hour < 0 or hour > 23:
        return False
    return True


def is_valid_minute(minute: int):
    if minute < 0 or minute > 59:
        return False
    return True


def get_date_from_shortcut(this_week: bool, weekday_num: int):
    """
    Params:
        - this_week (bool): True if this week, False if next week
        - weekday_num (int): 0 ~ 6, referring to monday ~ sunday
    """
    if not this_week:
        weekday_num += 7
        
    current_weekday_num = datetime.now().weekday()
    day_offset = weekday_num - current_weekday_num
    deadline_date = datetime.now() + timedelta(days=day_offset)
    
    return deadline_date.year, deadline_date.month, deadline_date.day


def get_date_from_offset(offset: int):
    deadline_date = datetime.now() + timedelta(days=offset)
    return deadline_date.year, deadline_date.month, deadline_date.day
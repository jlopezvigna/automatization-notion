from datetime import datetime, timedelta


def get_first_and_last_day_of_month(current_day=datetime.now()):
    year = current_day.year
    month = current_day.month
    first_day = datetime(year, month, 1)

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    last_day = datetime(next_year, next_month, 1) - timedelta(days=1)

    iso_first_day = first_day.strftime('%Y-%m-%d')
    iso_last_day = last_day.strftime('%Y-%m-%d')

    return iso_first_day, iso_last_day

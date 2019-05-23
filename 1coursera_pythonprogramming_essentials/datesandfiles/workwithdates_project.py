"""
Project-Collection of functions to process dates.
"""

import datetime


def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.

    >>> days_in_month(2018, 12)
    31
    >>> days_in_month(2019, 2)
    28
    >>> days_in_month(2016, 2)
    29
    >>> days_in_month(2019, 1)
    31
    >>> days_in_month(2018,3)
    31
    """

    if month >= 12:
        first_day_in_month = datetime.date(year, month, day=1)
        first_day_in_next_month = datetime.date(year + 1, month-11, day=1)
        return (first_day_in_next_month - first_day_in_month).days
    else:
        first_day_in_month = datetime.date(year, month, day=1)
        first_day_in_next_month = datetime.date(year, month + 1, day=1)
    return (first_day_in_next_month - first_day_in_month).days


def is_valid_date(year, month, day):
    """
    Inputs:
      year  - an integer representing the year
      month - an integer representing the month
      day   - an integer representing the day

    Returns:
      True if year-month-day is a valid date and
      False otherwise
    >>> is_valid_date(2019, 3, 1)
    True
    >>> is_valid_date(2018,3,32)
    False
    >>> is_valid_date(100000,3,28)
    False
    >>> is_valid_date(2018,13,1)
    False
    """
    is_valid_year = datetime.MINYEAR <= year <= datetime.MAXYEAR
    is_valid_month = 1 <= month <= 12
    if is_valid_year and is_valid_month:
        is_valid_day = 1 <= day <= days_in_month(year, month)
        if is_valid_day:
            return True
        else:
            return False
    else:
        return False


def days_between(year1, month1, day1, year2, month2, day2):
    """
    Inputs:
      year1  - an integer representing the year of the first date
      month1 - an integer representing the month of the first date
      day1   - an integer representing the day of the first date
      year2  - an integer representing the year of the second date
      month2 - an integer representing the month of the second date
      day2   - an integer representing the day of the second date

    Returns:
      The number of days from the first date to the second date.
      Returns 0 if either date is invalid or the second date is
      before the first date.
    >>> days_between(2019,1,1,2019,1,1)
    0
    >>> days_between(2019,1,1,2019,1,30)
    29
    >>> days_between(2019,1,1,2008,1,1)
    0
    >>> days_between(2019,1,1,2019,13,1)
    0
    >>> days_between(2019,1,32,2020,1,1)
    0
    """
    if is_valid_date(year1, month1, day1) and is_valid_date(year2, month2, day2):
        date_days_1 = datetime.datetime(year1, month1, day1)
        date_days_2 = datetime.datetime(year2, month2, day2)
        if date_days_1 < date_days_2:
            days_num = (date_days_2 - date_days_1).days
            return days_num
        else:
            return 0
    else:
        return 0


def age_in_days(year, month, day):
    """
    Inputs:
      year  - an integer representing the birthday year
      month - an integer representing the birthday month
      day   - an integer representing the birthday day

    Returns:
      The age of a person with the input birthday as of today.
      Returns 0 if the input date is invalid or if the input
      date is in the future.
    #>>> age_in_days(2016, 12, 31)
    #753
    #>>> age_in_days(2019,1,1)
    #22
    #>>> age_in_days(2019,12,3)
    #0
    #>>> age_in_days(2018, 13, 1)
    #0
    """
    today = datetime.date.today()
    if is_valid_date(year, month, day):
        if days_between(year, month, day, today.year, today.month, today.day) > 0:
            age_days = days_between(year, month, day, today.year, today.month, today.day)
            return age_days
        else:
            return 0
    else:
        return 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()

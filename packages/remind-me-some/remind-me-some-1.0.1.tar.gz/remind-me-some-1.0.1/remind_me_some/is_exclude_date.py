"""Check if a date should be excluded."""

from datetime import date
from holidays import UnitedStates as CountryHolidayCalendar
import logging


logger = logging.getLogger(__name__)


def is_exclude_date(
        date_: date,
        is_exclude_holidays: bool = True,
        is_exclude_weekends: bool = True,
        is_exclude_friday: bool = False,
) -> bool:
    """Return True if a date should be excluded.

    :param date_:
        The date to consider.
    :param is_exclude_holidays:
        True if you would like to exclude holidays.
    :param is_exclude_weekends:
        True if you would like to exclude weekends.
    :param is_exclude_friday:
        True if you would like to exclude Fridays.
    :return: True if the date should be excluded; false otherwise.
    """
    def _is_holiday(_date: date):

        return _date in CountryHolidayCalendar()

    def _is_weekend(_date: date):
        return _date.weekday() in [5, 6]  # saturday and sunday's codes

    def _is_friday(_date: date):
        return _date.weekday() == 4  # friday's codes

    if is_exclude_holidays:
        if _is_holiday(date_):
            logger.debug(f"{date_} is a holiday")
            return True
    if is_exclude_weekends:
        if _is_weekend(date_):
            logger.debug(f"{date_} is a weekend")
            return True
    if is_exclude_friday:
        if _is_friday(date_):
            logger.debug(f"{date_} is a friday")
            return True
    return False

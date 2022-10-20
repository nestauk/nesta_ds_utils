import datetime
import sys
import numpy as np


def parse_date_string(date_string: str, _format: str = "%Y-%m-%d") -> datetime.datetime:
    """parses a date string into a datetime object

    Args:
        date_string (str): string describing a date.
        _format (str, optional): date format. Defaults to "%Y-%m-%d".
        For additional date format options refer to `datetime documentation <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_

    Returns:
        datetime.datetime: date in datetime format if date_string matches date format,
        otherwise returns None
    """
    try:
        return datetime.datetime.strptime(date_string, _format)

    except ValueError:
        sys.stderr.write(
            "Date string {} did not match date format {}".format(date_string, _format)
        )
        return np.nan

    except TypeError:
        sys.stderr.write(
            "argument {} passed as date_string was type {} not string".format(
                date_string, type(date_string)
            )
        )
        return np.nan


def make_year(date: datetime.datetime) -> int:
    """Extracts year from a datetime.datetime object"""
    try:
        return int(date.year)

    except AttributeError:
        sys.stderr.write(
            "argument {} passed as datetime was type {} not datetime.datetime".format(
                date, type(date)
            )
        )
        return np.nan

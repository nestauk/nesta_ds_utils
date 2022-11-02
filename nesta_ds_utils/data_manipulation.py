import datetime
from http.client import _DataType
import sys
import numpy as np
from typing import Union


def parse_date_string(
    date_string: str,
    format: Union[str, list] = "%Y-%m-%d",
    error_value: Union[float, str] = np.nan,
) -> datetime.datetime:
    """parses a date string into a datetime object

    Args:
        date_string (str): string describing a date.
        format (str or list, optional): date format or list of possible date formats. Defaults to "%Y-%m-%d".
        For additional date format options refer to `datetime documentation <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.
        error_value (float or str, optional): value to use for null or improperly formatted values. Defaults to numpy.nan.

    Returns:
        datetime.datetime: date in datetime format if date_string matches date format,
        otherwise returns None.
    """
    if isinstance(format, str):
        try:
            return datetime.datetime.strptime(date_string, format)

        except ValueError:
            sys.stderr.write(
                "Date string {} did not match date format {}".format(
                    date_string, format
                )
            )
            return error_value

        except TypeError:
            sys.stderr.write(
                "argument {} passed as date_string was type {} not string".format(
                    date_string, type(date_string)
                )
            )
            return error_value

    else:
        for format_option in format:
            try:
                return datetime.datetime.strptime(date_string, format)

            except TypeError:
                sys.stderr.write(
                    "argument {} passed as date_string was type {} not string".format(
                        date_string, type(date_string)
                    )
                )
                return error_value

            except ValueError:
                continue
        return error_value


def make_year(date: datetime.datetime) -> int:
    """Extracts year from a datetime.datetime object."""
    try:
        return int(date.year)

    except AttributeError:
        sys.stderr.write(
            "argument {} passed as datetime was type {} not datetime.datetime".format(
                date, type(date)
            )
        )
        return np.nan

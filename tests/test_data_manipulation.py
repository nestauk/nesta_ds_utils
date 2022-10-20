import datetime
import pytest
import sys
import numpy as np

sys.path.insert(1, "nesta_ds_utils/")
import data_manipulation


def test_str_to_datetime():
    """tests that when a string is passed to parse_date_string following the default format
    it returns a datetime object
    """
    date = data_manipulation.parse_date_string("2022-10-10")
    assert isinstance(date, datetime.datetime)


def test_str_to_datetime_format():
    """tests that when a string is passed to parse_date_string with a specified format
    different from the default it returns a datetime object
    """
    date = data_manipulation.parse_date_string("10/10/2022", _format="%m/%d/%Y")
    assert isinstance(date, datetime.datetime)


def test_str_to_datetime_incorrect_format():
    """tests that when a string is passed to parse_date_string in the incorrect format it returns NaN"""
    date = data_manipulation.parse_date_string("10/10/2022")
    assert np.isnan(date)


def test_nonstring_to_datetime():
    """tests that when a non-string is passed to parse_date_string it returns NaN"""
    date = data_manipulation.parse_date_string(None)
    assert np.isnan(date)


def test_datetime_to_year():
    """tests that when a datetime object is passed to make_year it returns a year"""
    date = data_manipulation.parse_date_string("2022-10-10")
    year = data_manipulation.make_year(date)
    assert year == 2022


def test_string_to_year():
    """tests that when a string is passed to make_year it returns np"""
    year = data_manipulation.make_year("2022-10-10")
    assert np.isnan(year)

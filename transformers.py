import re
from decimal import Decimal

import pandas as pd


def currency_transformer(
        value: str | int | float,
        prefix: str="",
        suffix: str="",
        decimal_places: int=2,
        rounded: bool=True,
        normalize: bool=True
    ) -> str:
    """
    Helper function for transforming currency values

    :param str value: Value to be transformed
    :param str prefix: Prefix to be added to result value
    :param str suffix: Suffix to be added to result value
    :param int decimal_places: Decimal places to keep after transform
    :param bool rounded: If value should be rounded
    :param bool normalize: If decimal place zeroes should be removed
    """
    val = value

    if isinstance(value, str):
        pattern = r"[+-]?(?:\d+|\d{1,3}(?:,\d{3})*)(?:\.\d*)?"
        val = "".join(re.findall(pattern, val))

    val = Decimal(val)

    # Round
    if rounded: val = round(val, decimal_places)
    # Normalize
    if normalize: val = format(val.normalize(), "f")

    return f"{prefix}{val}{suffix}"


def dimension_transformer(
        value: str | int | float,
        normalize: bool=True,
        prefix: str="",
        suffix: str=""
    ) -> str:
    """
    Helper function for transforming dimension values

    :param str|int|float value: Value to be transformed
    :param bool normalize: If decimal place zeroes should be removed
    :param str prefix: Prefix to be added to result value
    :param str suffix: Suffix to be added to result value
    """
    if not isinstance(value, str):
        return ""

    value = Decimal(value)

    if normalize:
        value = format(value.normalize(), "f")

    return f"{prefix}{value}{suffix}"
    

def country_transformer(country: str) -> str:
    """
    Get country code of given country

    :param str country: Country full name
    """
    if not isinstance(country, str):
        return ""

    # https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
    country_map = {
        "china": "CHN",
        "india": "IND",
        "indonesia": "IDN",
        "philippines": "PHL",
        "thailand": "THA",
        "vietnam": "VNM"
    }

    return country_map.get(country.lower(), "")


def boolean_transformer(value: str) -> bool | None:
    """
    Helper function to convert yes/no values to native python boolean

    :param str value: String to convert
    """
    if isinstance(value, str):
        if "yes" in value.lower(): return True
        elif "no" in value.lower(): return False


def date_transformer(value: str) -> str | None:
    """
    Helper function to format date string into ISO format

    :param str value: Date string
    """
    value = pd.to_datetime(value)
    date = value.date()

    return date.isoformat()

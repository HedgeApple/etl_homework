import logging
import pandas as pd
from map_cols import (add_new_columns, column_order,
                      generate_column_mapping)


def process_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the columns of the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    logging.info("Processing columns...")
    df = df.copy()
    df = convert_units(df)
    df['prop_65'] = map_prop65(df)
    df = rename_columns(df)
    df = add_new_columns(df)
    df = format_columns(df)
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename the columns of the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns.
    """
    logging.info("Renaming columns...")
    column_mapping = generate_column_mapping(df)
    column_mapping['prop_65'] = 'prop_65'
    df.rename(columns=column_mapping, inplace=True)
    return df[column_mapping.values()]


def format_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format the columns of the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with formatted columns.
    """
    logging.info("Formatting columns...")
    df['ean13'] = df['ean13'].apply(format_ean)

    df['product__country_of_origin__alpha_3'] = df[
        'product__country_of_origin__alpha_3'].apply(format_country)
    df['cost_price'] = df['cost_price'].replace(
        {'\\$': '', ',': ''}, regex=True).astype(float)
    df['min_price'] = df['min_price'].replace(
        {'\\$': '', ',': ''}, regex=True).astype(float)
    df['cost_price'] = df['cost_price'].round(2)
    df['min_price'] = df['min_price'].round(2)
    return df


def order_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Order the columns of the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with ordered columns.
    """
    logging.info("Ordering columns...")
    columns = column_order()
    return df[columns]


def map_prop65(df: pd.DataFrame) -> pd.Series:
    """
    Map the Prop65 status based on the existence of
    California label URLs.

    Args:
        df (pd.DataFrame): Dataframe

    Returns:
        pd.Series: A boolean Series indicating the Prop65 status.
    """
    return df['url california label (jpg)'].notna() | df[
        'url california label (pdf)'].notna()


def format_ean(ean: int) -> str:
    """
    Format the EAN number.

    Args:
        ean (int): The input EAN number

    Returns:
        str: The formatted EAN number.
    """
    try:
        if ean < 0:
            return ""
        ean_str = str(int(ean)).zfill(12)
    except ValueError:
        return ""
    ean_13 = f"0{ean_str[:2]}-{ean_str[2:11]}-{ean_str[11]}"
    return ean_13


def format_country(country: str) -> str:
    """
    Format the country code.

    Args:
        country (str): The input country name.

    Returns:
        str: The formatted country code.
    """
    country_mapping = {
        'China': 'CHN',
        'India': 'IND',
        'Indonesia': 'IDN',
        'Phillipines': 'PH',
        'Thailand': 'TH',
        'Vietnam': 'VN'
    }
    return country_mapping.get(country, country)


def convert_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert the units of the weight and dimension columns
    in the DataFrame.

    Args:
        df (pd.DataFrame): Dataframe

    Returns:
        pd.DataFrame: The DataFrame with converted units.
    """
    for column in df.columns:
        if 'weight' in column and 'pounds' not in column:
            if 'kg' in column or 'kilograms' in column:
                df[column] = df[column] * 2.20462
            elif 'g' in column or 'grams' in column:
                df[column] = df[column] * 0.00220462
        elif ('length' in column or 'height' in column or 'width' in column
              ) and 'inches' not in column:
            if 'cm' in column or 'centimeters' in column:
                df[column] = df[column] * 0.393701
            elif 'm' in column or 'meters' in column:
                df[column] = df[column] * 39.3701
    return df

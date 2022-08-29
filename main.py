import pandas as pd

raw_df = pd.read_csv(r'homework.csv', low_memory=False)
columns = raw_df.columns.to_list()
formatted_dataframe = raw_df.copy(deep=True)


"""Prices | Width | Weight columns | Volume(ft to in)"""


def clear_number(value, volume=False):
    """This function recieves a raw number and removes any strange characters from it."""
    buf = str(value)
    try:
        value = "".join(filter(lambda x: x if x.isdigit()
                               or x == '.' or x == ',' else None, buf))
        value = value.replace(',', '.')
        if volume:
            return round((float(value) * 1728), 2)
        else:
            return round(float(value), 2)
    except ValueError:
        return 0.0


def normalize_number_fields(number_columns):
    for column in number_columns:
        if 'volume' in column:
            formatted_dataframe[column] = raw_df[column].apply(
                lambda x: clear_number(x, volume=True) if x != 'nan' else None)
            formatted_dataframe[column] = formatted_dataframe[column].fillna(
                0.0)

        else:
            formatted_dataframe[column] = raw_df[column].apply(
                lambda x: clear_number(x) if x != 'nan' else None)
            formatted_dataframe[column] = formatted_dataframe[column].fillna(
                0.0)


"""Date fields"""


def normalize_date_fields(date_cols):
    for column in date_cols:
        formatted_dataframe[column] = pd.to_datetime(
            raw_df[column]).dt.strftime('%Y-%m-%d')
        formatted_dataframe[column] = formatted_dataframe[column].fillna(0.0)


"""Fields asked to be considered as string (ean, upc, gtin)"""


def normalize_str_fields(string_cols):
    for column in string_cols:
        formatted_dataframe[column] = raw_df[column].astype('string')
        formatted_dataframe[column] = formatted_dataframe[column].fillna('')


# """Number columns"""
keywords = ['$', 'width', 'pounds', 'weight', 'inches', 'volume']
number_cols = [
    column for keyword in keywords for column in columns if keyword in column]

# """Date columns"""
date_fields_cols = list(filter(lambda x: x if 'date' in x else None, columns))

# """Fields that were asked to be considered as string"""
keywords = ['UPC', 'upc', 'GTIN', 'Gtin', 'EAN', 'ean']
string_cols = [
    column for keyword in keywords for column in columns if keyword in column]

# Data cleanse:
normalize_number_fields(number_cols)
normalize_date_fields(date_fields_cols)
normalize_str_fields(string_cols)
formatted_dataframe.to_csv('formatted.csv')

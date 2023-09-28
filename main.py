import logging
import pandas as pd
from map_cols import (generate_column_mapping, format_ean13,
                      add_new_columns, column_order,
                      country_mapping)


def process_file(filename: str, processed_file: str) -> None:
    try:
        homework_df = pd.read_csv(filename, low_memory=False)
        # column mapping
        column_mapping = generate_column_mapping(homework_df)
        homework_df.rename(columns=column_mapping, inplace=True)
        new_columns = set(column_mapping.values())
        if new_columns.issubset(homework_df.columns):
            homework_df = homework_df[list(new_columns)]
        else:
            missing_columns = new_columns.difference(homework_df.columns)
            logging.error("Warning: The following columns are missing:"
                          f"{missing_columns}")
        homework_df = add_new_columns(homework_df)
        # converting ean to str and matching to the format in example.csv
        homework_df['ean13'] = homework_df['ean13'].apply(format_ean13)
        homework_df['product__country_of_origin__alpha_3'] = homework_df[
            'product__country_of_origin__alpha_3'].map(country_mapping)
        # removing $ sign from currency and putting it two decimal places
        homework_df['cost_price'] = homework_df['cost_price'].replace(
            {'\$': '', ',': ''}, regex=True).astype(float)
        homework_df['min_price'] = homework_df['min_price'].replace(
            {'\$': '', ',': ''}, regex=True).astype(float)
        homework_df['cost_price'] = homework_df['cost_price'].round(2)
        homework_df['min_price'] = homework_df['min_price'].round(2)
        columns = column_order()
        homework_df = homework_df[columns]
        homework_df.to_csv(processed_file, index=False)
    except Exception as err:
        logging.error(f"An error occurred: {err}")


if __name__ == '__main__':
    process_file("files/homework.csv", "files/formatted9.csv")

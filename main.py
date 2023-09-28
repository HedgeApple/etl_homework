import logging
import pandas as pd
from map_cols import (add_new_columns, column_order, country_mapping,
                      format_ean, generate_column_mapping, map_prop65)


def process_file(filename: str, processed_file: str) -> None:
    try:
        # reading the file
        homework_df = pd.read_csv(filename, low_memory=False)
        # column mapping
        homework_df['prop_65'] = map_prop65(homework_df)
        column_mapping = generate_column_mapping(homework_df)
        homework_df.rename(columns=column_mapping, inplace=True)
        column_mapping['prop_65'] = 'prop_65'
        homework_df = homework_df[column_mapping.values()]
        homework_df = add_new_columns(homework_df)

        # converting ean to str and matching to the format in example.csv
        homework_df['ean13'] = homework_df['ean13'].apply(format_ean)

        # converting country names to their alpha-3 codes
        homework_df['product__country_of_origin__alpha_3'] = homework_df[
            'product__country_of_origin__alpha_3'].map(country_mapping)

        # removing $ sign from currency and putting it two decimal places
        homework_df['cost_price'] = homework_df['cost_price'].replace(
            {'\\$': '', ',': ''}, regex=True).astype(float)
        homework_df['min_price'] = homework_df['min_price'].replace(
            {'\\$': '', ',': ''}, regex=True).astype(float)
        homework_df['cost_price'] = homework_df['cost_price'].round(2)
        homework_df['min_price'] = homework_df['min_price'].round(2)

        # ordering the columns
        columns = column_order()
        homework_df = homework_df[columns]

        # writing File to Csv
        homework_df.to_csv(processed_file, index=False)
    except Exception as err:
        logging.error(f"An error occurred: {err}")


if __name__ == '__main__':
    process_file("files/homework.csv", "files/formatted.csv")

import logging
import pandas as pd
from map_cols import generate_column_mapping, format_ean13


country_mapping = {
    'China': 'CHN',
    'India': 'IND',
    'Indonesia': 'IDN',
    'Phillipines': 'PH',
    'Thailand': 'TH',
    'Vietnam': 'VN'
}


def process_file(filename: str, processed_file: str,
                 n_boxes: int, n_bullets: int) -> None:
    try:
        homework_df = pd.read_csv(filename, low_memory=False)
        # column mapping
        column_mapping = generate_column_mapping(n_boxes=n_boxes,
                                                 n_bullets=n_bullets)
        homework_df.rename(columns=column_mapping, inplace=True)
        homework_df = homework_df[column_mapping.values()]

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
        homework_df.to_csv(processed_file, index=False)
    except Exception as err:
        logging.error(f"An error occurred: {err}")


if __name__ == '__main__':
    process_file("files/homework.csv", "files/formatted.csv",
                 n_boxes=3, n_bullets=7)

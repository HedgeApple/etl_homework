import logging
import pandas as pd
from format_cols import process_columns, order_columns


def process_file(filename: str, processed_file: str) -> None:
    """
    Process the input file and save the result to the output file.

    Args:
        filename (str): The name of the input file.
        processed_file (str): The name of the output file.
    """
    try:
        logging.info(f"Processing file: {filename}")
        homework_df = pd.read_csv(filename, low_memory=False)
        homework_df = process_columns(homework_df)
        homework_df = order_columns(homework_df)
        homework_df.to_csv(processed_file, index=False)
        logging.info(f"File processed successfully: {processed_file}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")


if __name__ == '__main__':
    process_file("files/homework.csv", "files/formatted.csv")

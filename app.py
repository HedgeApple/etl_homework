import pandas as pd
import logging
from transformations import transforms


# ------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# ------------------------------------------


def read_dataset(file_path=None):
    data_frame = pd.read_csv(
        filepath_or_buffer=file_path
    )

    if not data_frame.empty:
        logger.info("DataFrame Retrived Successfully")
        return data_frame
    
    logging.error("Error Retruning Dataframe")
    return False

# ------------------------------------------

def implement_transforms(dataframe=None):

    logger.info("Processing Data Transformations")

    # UPC TRANSFORMATION 
    dataframe["upc"] = dataframe["upc"].apply(transforms().upc_transform)

    # DATE TRANSFORMATION
    dataframe["system creation date"] = dataframe["system creation date"].apply(transforms().date_transform)

    # CURRENCY TRANSFORMATION
    dataframe["wholesale ($)"] = dataframe["wholesale ($)"].apply(transforms().currency_transfrom)
    dataframe["map ($)"] = dataframe["map ($)"].apply(transforms().currency_transfrom)
    dataframe["msrp ($)"] = dataframe["msrp ($)"].apply(transforms().currency_transfrom)
    dataframe["chain price ($)"] = dataframe["chain price ($)"].apply(transforms().currency_transfrom)
    dataframe["replacement glass price ($)"] = dataframe["replacement glass price ($)"].apply(transforms().currency_transfrom)
    dataframe["replacement crystal price ($)"] = dataframe["replacement crystal price ($)"].apply(transforms().currency_transfrom)

    # DIMENSION TRANSFORMATION
    # [TODO]


    # WEIGHT TRANSFORMATION
    # [TODO]

    return dataframe

# ------------------------------------------

def formatted_csv(dataframe=None):

    logger.info("Creating Formatted CSV File")

    dataframe.to_csv(
        path_or_buf=r"formatted_file\formatted.csv",
        index=False,
    )

# ------------------------------------------

def main():
    df = read_dataset(file_path="homework.csv")
    df = implement_transforms(dataframe=df)

    formatted_csv(dataframe=df)

# ------------------------------------------

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------
# End of File
# ----------------------------------------------------------------------


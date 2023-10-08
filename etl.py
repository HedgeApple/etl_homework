import json

import structlog
import pandas as pd


log = structlog.get_logger()

direct_mapping = {
    "manufacturer_sku": "item number",
    "ean13": "upc",
    "product__multipack_quantity": "min order qty",
    "cost_price": "wholesale ($)",
    "min_price": "map ($)",
    "product__title": "description",
    "product__description": "long description",
    "product__brand__name": "brand",
    "attrib__outdoor_safe": "outdoor",
    "product__product_class__name": "item category",
    "width": "item width (inches)",
    "height": "item height (inches)",
    "weight": "item weight (pounds)",
    "attrib__material": "item materials",
    "attrib__color": "primary color family",
    "attrib__finish": "item finish",
    "product__styles": "item style",
    "attrib__distressed_finish": "item substyle",
    "attrib__designer": "item collection",
    "boxes__0__width": "carton 1 width (inches)",
    "boxes__0__length": "carton 1 length (inches)",
    "boxes__0__height": "carton 1 height (inches)",
    "boxes__0__weight": "carton 1 weight (pounds)",
    "boxes__1__width": "carton 2 width (inches)",
    "boxes__1__length": "carton 2 length (inches)",
    "boxes__1__height": "carton 2 height (inches)",
    "boxes__1__weight": "carton 2 weight (pounds)",
    "boxes__2__width": "carton 3 width (inches)",
    "boxes__2__length": "carton 3 length (inches)",
    "boxes__2__height": "carton 3 height (inches)",
    "boxes__2__weight": "carton 3 weight (pounds)",
    "attrib__ul_certified": "safety rating",
    "attrib__kit": "conversion kit option",
    "attrib__switch_type": "switch type",
    "attrib__cord_length": "cord length (inches)",
    "attrib__arm_height": "furniture arm height (inches)",
    "attrib__seat_height": "furniture seat height (inches)",
    "attrib__weight_capacity": "furniture weight capacity (pounds)",
    "product__country_of_origin__alpha_3": "country of origin",
    "product__bullets__0": "selling point 1",
    "product__bullets__1": "selling point 2",
    "product__bullets__2": "selling point 3",
    "product__bullets__3": "selling point 4",
    "product__bullets__4": "selling point 5",
}

columns_to_json = {
    'attrib_shades': ['shade/glass description',
                      'shade/glass materials',
                      'shade/glass finish',
                      'shade/glass width at top (inches)',
                      'shade/glass width at bottom (inches)',
                      'shade/glass height (inches)',
                      'shade shape',
                      'harp/spider']
}


def convert_to_json(row, columns):
    """
    To group related columns and store them as JSON string.
    :param row: Dataframe row
    :param columns: List of related column names
    :return: Json formatted string
    """
    json_data = {}
    for column in columns:
        value = row[column]
        if not pd.isna(value):
            json_data[column] = value
        else:
            json_data[column] = ""
    return json.dumps(json_data, indent=4)


def csv_to_df():
    """
    Reading CSV file
    :return: pandas dataframe for homework.csv
    and example.csv
    """
    log.info('Reading csv files to create dataframes')
    homework_df = pd.read_csv('homework.csv', low_memory=False)
    homework_df.dropna(axis=1, how='all')
    example_df = pd.read_csv('example.csv')
    example_df.drop(index=example_df.index, inplace=True)
    log.info('Dataframes created')
    return homework_df, example_df


def transform_df(original_df, formatted_df):
    """
    To create dataframe for formatted.csv
    """
    new_rows = {}
    for index, row in original_df.iterrows():
        log.info(f'Importing {index} of {len(original_df)} ')
        for key, value in direct_mapping.items():
            if key in formatted_df.columns:
                new_rows[key] = row[value]
            else:
                raise ValueError(f"The column {key} doesn't exists.")
        new_rows['attrib__shade'] = convert_to_json(row, columns_to_json['attrib_shades'])
        formatted_df.loc[len(formatted_df)] = new_rows
    return formatted_df


def main():
    original_df, formatted_df = csv_to_df()
    formatted_df = transform_df(original_df, formatted_df)
    formatted_df.to_csv('formatted.csv', index=False)
    log.info('Successfully created formatted.csv file')


if __name__ == '__main__':
    main()
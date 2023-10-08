import re
import json

import requests
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


def get_alpha3_code(country_name):
    """
    To get alpha3code from  OpenDataSoft API.
    :param country_name:
    :return: Alpha3code or country name in case alpha3code couldn't be retrieved.
    """
    url = (f"https://public.opendatasoft.com/"
           f"api/explore/v2.1/catalog/datasets/countries-codes/records?"
           f"select=iso3_code&where=label_en='{country_name}'&limit=1")
    try:
        response = requests.get(url)
        response.raise_for_status()
        country = response.json()['results'][0]['iso3_code']
        log.info(f'Retrieved alpha3code for {country_name} is {country}')
        return country
    except IndexError:
        log.warning(f'Could not find Alpha3code for country {country_name}.')
    except Exception as e:
        log.error(f"Unable to get alpha3 code for {country_name} due to the following error: {e}")
    log.warning(f"Returning country name, not it's Alpha3code.")
    return country_name


def csv_to_df():
    """
    Reading CSV file
    :return: pandas dataframe for homework.csv
    and example.csv
    """
    log.info('Reading csv files to create dataframes')
    homework_df = pd.read_csv('homework.csv', low_memory=False)
    example_df = pd.read_csv('example.csv')
    log.info('Dataframes created')
    return homework_df, example_df


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


def round_to_unit_of_accounting(num):
    if pd.isna(num):
        return num
    if isinstance(num, str):
        num = float(re.search(r'[-+]?\d*\.\d+|\d+', num).group())
    num = round(num, 2)
    return f"{num:.2f}"


def transform_df(original_df, formatted_df):
    """
    To create dataframe for formatted.csv
    """
    original_df.dropna(axis=1, how='all')
    original_df['upc'] = (original_df['upc']
                          .apply(lambda x: str(int(x)) if not pd.isna(x) and not isinstance(x, str) else x))
    original_df['wholesale ($)'] = original_df['wholesale ($)'].apply(round_to_unit_of_accounting)
    original_df['map ($)'] = original_df['map ($)'].apply(round_to_unit_of_accounting)
    formatted_df.drop(index=formatted_df.index, inplace=True)

    countries = original_df['country of origin'].dropna().unique().tolist()
    alpha3code = {}
    for country in countries:
        alpha3code[country] = get_alpha3_code(country)
    original_df['country of origin'] = (original_df['country of origin']
                                        .apply(lambda x: alpha3code[x] if not pd.isna(x) else x))

    new_rows = {}
    for index, row in original_df.iterrows():
        log.info(f'Importing {index} of {len(original_df)}')
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

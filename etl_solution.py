import pandas as pd
import json

# Currency Transformation
def transform_currency(value):
    if isinstance(value, str):
        try:
            return round(float(value.replace('$', '').replace(',', '')), 2)
        except:
            return value
    return value

# Dimension Transformation
def transform_dimension(value, transform_units):

    value = str(value) if isinstance(value, float) else value.lower().strip()
    for unit in transform_units:
        if unit in value:
            value = float(value.replace(unit, ''))
            return value *  transform_units[unit]
        return float(value)

# Weight Transformation
def transform_weights(value, transform_units):
    value = str(value) if isinstance(value, float) else value.lower().strip()
    for unit in transform_units:
        if unit in value:
            value = float(value.replace(unit, ''))
            return value *  transform_units[unit]
    return float(value)

def transform_product_styles(value):
    if isinstance(value, str):
        try:
            return value.replace('/', ',').replace(' ', '')
        except:
            return value
    return value

def transform_country_origin(value, transform_units):
    for country in transform_units:
        if value in transform_units[country]:
            return country
    return value

def transformations(columns_to_transform, transform_logic, transform_units):
    function_name = transform_logic
    func = globals()[function_name]
    for col in columns_to_transform:
        f = (lambda value: func(value, transform_units)) if transform_units else (lambda value: func(value))
        homework_df[col] = homework_df[col].apply(f)

if __name__ == "__main__":
    # Open and read the JSON file
    with open('etl_conf.json', 'r') as file:
        ETL_CONF = json.load(file)
        COLUMN_MAPPER = ETL_CONF['column_mapping']
        TRANSFORMATIONS = ETL_CONF['transformations']

    #read the homework csv into a dataframe
    homework_df = pd.read_csv('homework.csv', low_memory=False)

    #Merge Product styles
    homework_df['item style'] = homework_df['item style'] + ',' + homework_df['item substyle'] + ',' + homework_df['item substyle 2']

    # Date Transformation - ISO 8601
    homework_df['system creation date'] = pd.to_datetime(homework_df['system creation date'], format='%m/%d/%y').dt.strftime('%Y-%m-%d')

    # UPC/EAN Transformation
    homework_df['upc'] = homework_df['upc'].astype(str).str.rstrip('.0')

    homework_df['item style'] = homework_df['item style'].apply(transform_product_styles)

    for transform in TRANSFORMATIONS:
        transformations(TRANSFORMATIONS.get(transform, {}).get('columns_to_transform'),
                        TRANSFORMATIONS.get(transform, {}).get('tranform_logic'),
                        TRANSFORMATIONS.get(transform, {}).get('units'))

    formatted_df_updated = homework_df[list(COLUMN_MAPPER.keys())].rename(columns=COLUMN_MAPPER)
    formatted_df_updated.to_csv('formatted.csv', index=False)
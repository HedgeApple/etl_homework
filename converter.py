import pandas as pd
import numpy as np

import pycountry as pycountry

# Define the input and output file paths
input_file = 'homework.csv'
output_file = 'formatted.csv'
return_df = None


def assign_dimensions(input_str):
    input_str = str(input_str)
    split_list = input_str.split("x")
    if len(split_list) == 1:
        split_list = input_str.split("*")
        if len(split_list) == 1:
            split_list = input_str.split("X")
            if len(split_list) == 1:
                return_df['attrib__seat_width'] = float(split_list[0])
    if len(split_list) == 2:
        return_df['attrib__seat_width'] = float(split_list[0])
        return_df['attrib__seat_depth'] = float(split_list[1])
    if len(split_list) == 3:
        return_df['attrib__seat_width'] = float(split_list[0])
        return_df['attrib__seat_depth'] = float(split_list[2])


def get_styles(input_str):
    input_str = str(input_str)
    splitList_2 = input_str.split(' / ')
    splitList = str(input_data_frame['item substyle']).split(' / ')
    splitList_1 = str(input_data_frame['item substyle 2']).split(' / ')
    splitList += splitList_1
    splitList = splitList_2 + splitList
    output = ""
    for i in range(len(splitList)):
        if(i == len(splitList) - 1):
            output += splitList[i]
        elif i == len(splitList) - 2:
            output += splitList[i] + " & "
        else:
            output += splitList[i] + " "


def get_size(input_str):
    input_str = str(input_str)
    input_str = input_str.lower()
    if "small" in input_str:
        return "Small"
    if "large" in input_str:
        return "Large"

def is_hardwired(input_str):
    if input_str == "Hardwired":
        return "Yes"
    return ""

def is_ul(input_str):
    if input_str == "UL":
        return "TRUE"
    return ""


def is_distressed(input_str):
    input_str = str(input_str)
    if "Distressed" in input_str:
        # Wasn't sure if this should be binary or return the finish?
        return "Yes"
    return ""


def convert_country_to_abbreviation(country_name):
    try:
        country_name = str(country_name)
        country = pycountry.countries.search_fuzzy(country_name)
        return country[0].alpha_3
    except LookupError:
        return country_name  # Return the original name if not found


def convert_currency(currency_str):
    try:
        # Remove commas and dollar signs, then convert to float and round to 2 decimal places
        currency_str = str(currency_str)
        currency_str = currency_str.replace(',', '').replace('$', '')
        currency_float = round(float(currency_str), 2)
        return currency_float
    except ValueError:
        # Handle invalid currency values as needed
        return None


# Define a function to perform the transformations
def transform_data(input_df):
    global return_df
    return_df = pd.DataFrame()

    # Handle UPC / GTIN / EAN as strings
    return_df['manufacturer_sku'] = input_df['item number'].astype(str)

    # Even handling this as a string shows as a number in Excel
    return_df['ean13'] = input_df['upc'].astype(str)
    return_df['weight'] = input_df['item weight (pounds)'].astype(np.float64)
    return_df['length'] = input_df['item depth (inches)'].astype(np.float64)
    return_df['width'] = input_df['item width (inches)'].astype(np.float64)
    return_df['height'] = input_df['item height (inches)'].astype(np.float64)

    # could not find a way to populate this from the given csv file
    return_df['prop_65'] = ""

    # Round currency to cents and assume USD
    return_df['cost_price'] = input_df['wholesale ($)'].apply(convert_currency)

    # could not find a way to populate this from the given csv file
    return_df['min_price'] = ""

    # could not find a way to populate this from the given csv file
    return_df['made_to_order'] = ""

    return_df['product__product_class__name'] = input_df['item category'].astype(str)
    return_df['product__brand__name'] = input_df['brand']
    return_df['product__title'] = input_df['description']

    return_df['product__description'] = input_df['long description']
    return_df['product__bullets__0'] = input_df['selling point 1']
    return_df['product__bullets__1'] = input_df['selling point 2']
    return_df['product__bullets__2'] = input_df['selling point 3']
    return_df['product__bullets__3'] = input_df['selling point 4']
    return_df['product__bullets__4'] = input_df['selling point 5']
    return_df['product__bullets__5'] = input_df['selling point 6']
    return_df['product__bullets__6'] = input_df['selling point 7']

    # could not find a way to populate this from the given csv file
    return_df['product__configuration__codes'] = ""

    return_df['product__multipack_quantity'] = input_df['carton count']
    return_df['product__country_of_origin__alpha_3'] = input_df['country of origin'].apply(
        convert_country_to_abbreviation)

    # could not find a way to populate this from the given csv file
    return_df['product__parent_sku'] = ""

    return_df['attrib__arm_height'] = input_df['furniture arm height (inches)'].astype(np.float64)

    # could not find a way to populate this from the given csv file
    return_df['attrib__assembly_required'] = ""

    return_df['attrib__back_material'] = ""
    return_df['attrib__blade_finish'] = ""
    return_df['attrib__bulb_included'] = input_df['bulb 1 included']
    return_df['attrib__bulb_type'] = input_df['bulb 1 type']
    return_df['attrib__color'] = ""
    return_df['attrib__cord_length'] = input_df['cord length (inches)'].astype(np.float64)

    # could not find a way to populate this from the given csv file
    return_df['attrib__design_id'] = ""
    return_df['attrib__designer'] = ""

    return_df['attrib__distressed_finish'] = input_df['item finish'].apply(is_distressed)

    # could not find a way to populate this from the given csv file
    return_df['attrib__fill'] = ""

    return_df['attrib__finish'] = input_df['item finish']
    return_df['attrib__frame_color'] = input_df['primary color family']

    return_df['attrib__hardwire'] = input_df['switch type'].apply(is_hardwired)
    return_df['attrib__kit'] = input_df['conversion kit option']

    # could not find a way to populate this from the given csv file
    return_df['attrib__leg_color'] = ""
    return_df['attrib__leg_finish'] = ""

    return_df['attrib__material'] = input_df['item materials']
    return_df['attrib__number_bulbs'] = input_df['bulb 1 count']

    # could not find a way to populate this from the given csv file
    return_df['attrib__orientation'] = ""

    return_df['attrib__outdoor_safe'] = input_df['outdoor']

    # could not find a way to populate this from the given csv file
    return_df['attrib__pile_height'] = ""

    input_df['furniture seat dimensions (inches)'].apply(assign_dimensions)
    return_df['attrib__seat_height'] = input_df['furniture seat height (inches)']
    return_df['attrib__shade'] = input_df['shade/glass description']
    return_df['attrib__size'] = input_df['description'].apply(get_size)
    return_df['attrib__switch_type'] = input_df['switch type']
    return_df['attrib__ul_certified'] = input_df['safety rating'].apply(is_ul)

    # could not find a way to populate this from the given csv file
    return_df['attrib__warranty_years'] = ""

    return_df['attrib__wattage'] = input_df['bulb 1 wattage']

    # could not find a way to populate this from the given csv file
    return_df['attrib__weave'] = ""

    return_df['attrib__weight_capacity'] = input_df['furniture weight capacity (pounds)'].astype(np.float64)
    return_df['boxes__0__weight'] = input_df['carton 1 weight (pounds)']
    return_df['boxes__0__length'] = input_df['carton 1 length (inches)']
    return_df['boxes__0__height'] = input_df['carton 1 height (inches)']
    return_df['boxes__0__width'] = input_df['carton 1 width (inches)']
    return_df['boxes__1__weight'] = input_df['carton 2 weight (pounds)']
    return_df['boxes__1__length'] = input_df['carton 2 length (inches)']
    return_df['boxes__1__height'] = input_df['carton 2 height (inches)']
    return_df['boxes__1__width'] = input_df['carton 2 width (inches)']
    return_df['boxes__2__weight'] = input_df['carton 3 weight (pounds)']
    return_df['boxes__2__length'] = input_df['carton 3 length (inches)']
    return_df['boxes__2__height'] = input_df['carton 3 height (inches)']
    return_df['boxes__2__width'] = input_df['carton 3 width (inches)']
    return_df['boxes__3__weight'] = ""
    return_df['boxes__3__length'] = ""
    return_df['boxes__3__height'] = ""
    return_df['boxes__3__width'] = ""
    return_df['product__styles'] = input_df['item substyle'].apply(get_styles)

    return return_df


# Read the input CSV file into a DataFrame
input_data_frame = pd.read_csv(input_file)

# Perform the transformations
output_df = transform_data(input_data_frame)

# Save the transformed data to the output CSV file
output_df.to_csv(output_file, index=False)

print("Transformation completed. Output saved to", output_file)

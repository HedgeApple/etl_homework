# importing csv library to read and write from and to csv file
import csv
# importing pandas library to make easier computations to dataframe
import pandas as pd

# A function to convert upc column to ean13 as represented in the example.csv file
def getEan13(upc):
    # Adding a '0' at the start following with hyphen at specific intervals
    upc = "0" * (12 - len(upc)) + upc
    ean13 = "0" + upc[:2] + "-" + upc[2:11] + "-" + upc[11]
    return ean13


header_values_example = []
# Open the example.csv file and read the file data
with open('example.csv', 'r') as file_example:
    example_csv = csv.reader(file_example)
    header_values_example = next(example_csv)
    print(header_values_example)
    
    # using pandas to convert csv file data to dataframe and do necessary computations
    hw_dataframe = pd.read_csv("homework.csv", encoding="utf-8", low_memory=False)

    # date in ISO format
    hw_dataframe['system creation date'] = pd.to_datetime(hw_dataframe['system creation date'])
    hw_dataframe['system creation date'].map(lambda x: x.isoformat())

    # UPC / Gtin / EAN handled as strings
    hw_dataframe['upc'] = hw_dataframe['upc'].astype('str')

    hw_dataframe["upc"] = hw_dataframe["upc"].apply(getEan13)
    # print(hw_dataframe["upc"])

    # renaming the columns based on column names from example.csv
    hw_dataframe.rename(columns={
        'item number': 'manufacturer_sku',
        'upc': 'ean13',
        'item weight (pounds)': 'weight',
        'item depth (inches)':'length',
        'item width (inches)':'width', 
        'item height (inches)':'height',
        'wholesale ($)':'cost_price',
        'map ($)':'min_price',
        'item category': 'product__product_class__name',
        'brand': 'product__brand__name',
        'description': 'product__title',
        'long description': 'product__description',
        'selling point 1': 'product__bullets__0',
        'selling point 2': 'product__bullets__1', 
        'selling point 3': 'product__bullets__2', 
        'selling point 4': 'product__bullets__3', 
        'selling point 5': 'product__bullets__4', 
        'selling point 6': 'product__bullets__5', 
        'selling point 7': 'product__bullets__6', 
        'carton count': 'product__multipack_quantity', 
        'country of origin': 'product__country_of_origin__alpha_3', 
        'furniture arm height (inches)': 'attrib__arm_height', 
        'bulb 1 included': 'attrib__bulb_included', 
        'bulb 1 type': 'attrib__bulb_type', 
        'primary color family': 'attrib__color', 
        'cord length (inches)': 'attrib__cord_length', 
        'licensed by': 'attrib__designer', 
        'item finish': 'attrib__finish',  
        'conversion kit option': 'attrib__kit', 
        'item materials': 'attrib__material', 
        'bulb 1 count': 'attrib__number_bulbs', 
        'outdoor': 'attrib__outdoor_safe', 
        'max overall height (inches)': 'attrib__pile_height', 
        'furniture seat height (inches)': 'attrib__seat_height',  
        'furniture seat dimensions (inches)': 'attrib__size', 
        'switch type': 'attrib__switch_type', 
        'safety rating': 'attrib__ul_certified',  
        'bulb 1 wattage': 'attrib__wattage', 
        'furniture weight capacity (pounds)': 'attrib__weight_capacity', 
        'carton 1 weight (pounds)':'boxes__0__weight',
        'carton 1 length (inches)':'boxes__0__length',
        'carton 1 height (inches)':'boxes__0__height',
        'carton 1 width (inches)':'boxes__0__width',
        'carton 2 weight (pounds)':'boxes__1__weight',
        'carton 2 length (inches)':'boxes__1__length',
        'carton 2 height (inches)':'boxes__1__height',
        'carton 2 width (inches)':'boxes__1__width',
        'carton 3 weight (pounds)':'boxes__2__weight',
        'carton 3 length (inches)':'boxes__2__length',
        'carton 3 height (inches)':'boxes__2__height',
        'carton 3 width (inches)':'boxes__2__width', 
        'item style': 'product__styles' 
    }, inplace=True)


    hw_dataframe.to_csv("formatted.csv", index=False)



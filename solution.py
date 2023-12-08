## Goal: Code to analyze and transform data
## Input: Code reads data from `homework.csv` file passed in line 9
## Output: Code produces parsed output file to `solution.csv`
## Code by: Anna Fritz 

import pandas as pd
import numpy as np

#################################
# First thing is reading the data 
data= pd.read_csv("homework.csv", low_memory=False)
data.columns = data.columns.str.lower()

# we want to index on the item number 
data.set_index('item number', inplace=True)

#############################
#Change dates to use ISO 8601
def format_dates(df): 
    currency_columns = df.filter(like='date').columns
    for c in currency_columns: 
        data[c] = pd.to_datetime(data[c], format='%m/%d/%y')
        data[c] = data[c].apply(lambda x: x.isoformat())
    return df

data = format_dates(data)

##################################################
# Currency should be rounded to unit of accounting. 
# Assume USD for currency and round to cents.
def format_currency(df, c):
    df[c] = pd.to_numeric(df[c].replace('[\$,]', '', regex=True), errors='coerce')
    df[c] = df[c].round(2)
    df[c] = df[c].map('${:,.2f}'.format)
    return df

# Now we need to find which columns may contain a currency and format those 
def apply_format_currency(df):
    # Select columns that contain '($)' in the title
    currency_columns = df.filter(like='($)').columns
    # Apply the format_currency function to the selected columns
    for c in currency_columns: 
        df = format_currency(df,c)
    return df

data = apply_format_currency(data)

###################################
# convert any measurements to inches 
# For sake of the project, lets say things may be in inches, feet, or centimeters. The column title will include the label. 
# So we need to get the column that may contain length and convert them to inches 
def convert_dimensions_to_inches(df):
    conversion_factors_length = {'inches': 1, 'feet': 12, 'centimeters': 0.393701}

    # Identify columns with titles containing conversion factors
    dimension_columns = []
    for key, val in conversion_factors_length.items():
        dimension_columns.extend(df.filter(like=key).columns)

    # Convert to inches using conversion factors
    for column in dimension_columns:
        for key, val in conversion_factors_length.items():
            if key in column:
                df[column] = df[column].apply(lambda x: x * val)
    return df

data = convert_dimensions_to_inches(data)

##############################
# convert any weights to pounds
# Same thought process but now for weight... if you want to add more conversion factors you would just add them to the dictionary 
def convert_dimensions_to_pounds(df):
    conversion_factors_weight = {'pounds': 1, 'kilograms': 2.20462}

    # Identify columns with titles containing conversion factors
    dimension_columns = []
    for key, val in conversion_factors_weight.items():
        dimension_columns.extend(df.filter(like=key).columns)

    # Convert to inches using conversion factors
    for column in dimension_columns:
        for key, val in conversion_factors_weight.items():
            if key in column:
                df[column] = df[column].apply(lambda x: x * val)
    return df

data = convert_dimensions_to_pounds(data)

#######################################################
# handle UPC / Gtin / EAN should be handled as strings
def convert_lab_to_str(df):
    possible_columns = ['upc', 'gtin', 'ean']
    for column in possible_columns:
        if column in df.columns: 
            df[column] = df[column].astype(str)
    return df

data = convert_lab_to_str(data)

# floating points should be preserved 

#####################
# output file to csv
data.to_csv("solution.csv")
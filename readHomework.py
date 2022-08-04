# Using external library instead of the standard csv library provided in python
# pip install pandas
import pandas

CUBIC_INCHES_TO_CUBIC_FEET = 1728

# read_csv attributes used:
    # index_col ('item number'): specify which column to use for the DataFrame index
    # dtype (str): consider all data field types as string. This will preserve formating of the cell when reading. dtype will be overide when we specify which column we don't want as string
    # parse_dates ('system creation date'): This will overide dtype and convert 'system creation date' column to ISO 8601 Dates
df = pandas.read_csv('homework.csv', index_col='item number', dtype=str, parse_dates=['system creation date'])

# Fill all NaN with empty string
# Reason for NaN is because pandas mark emtpy cells with NaN. 
# I would like to have all empty cell be 0 but empty and 0 are two different concept. 
# Going to side with empty string to represent empty cell here feels safer.
df = df.fillna('')

# Currency column must be cleaned such as removing all '$' and ','. Reason to remove '$' because the column is 
# already marked with currency property. I'm also assuming this field in the backend database already has currency type. So having 
# '$' in the value doens't make sense.
# Assuming we are loading the output csv into postgres, removing unnecessary special characters can faciliate the data load.
currencyCol = ['wholesale ($)', 'map ($)', 'msrp ($)', 'chain price ($)', 'replacement glass price ($)', 'replacement crystal price ($)']
for col in currencyCol: 
    df[col] = [str(x).replace('$','').replace(',', '') for x in df[col]]

    # Rounding to the nearest cent to achieve 2 decimal places for currency columns.
    df[col] = [round(float(x), 2) if x != '' else x for x in df[col]]


# There were 3 columns that references cubic feet (carton 1 volume (cubic feet), carton2volumecubicfeet, carton 3 volume (cubic feet))
# Based on the requirement, we must convert these to cubic inches. But we need to create a new column with the correct names to reference the new data. 
# I'm settling on the names of carton 1 volume (cubic inch), carton2volumecubicinch, carton 3 volume (cubic inch)
df['carton 1 volume (cubic inch)'] = [float(x) * CUBIC_INCHES_TO_CUBIC_FEET if x != '' else x for x in df['carton 1 volume (cubic feet)']]
df['carton2volumecubicinch'] = [float(x) * CUBIC_INCHES_TO_CUBIC_FEET if x != '' else x for x in df['carton2volumecubicfeet']]
df['carton 3 volume (cubic inch)'] = [float(x) * CUBIC_INCHES_TO_CUBIC_FEET if x != '' else x for x in df['carton 3 volume (cubic feet)']]

# write to formatted.csv
df.to_csv('formatted.csv')
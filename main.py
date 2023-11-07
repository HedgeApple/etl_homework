import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)


def normalize_number(s):
    """
    Normalize a numeric string by removing currency symbols and commas.

    Args:
        s (str): The numeric string to be normalized.

    Returns:
        str: The normalized numeric string.

    Example:
        >>> normalize_number("$1,000,000")
        '1000000'
    """
    if '$' in s:
        s = s.replace('$', '')
    if ',' in s:
        s = s.replace(',', '')
    return s


def normalize_value(row, column):
    """
    Normalize a specific column value in a DataFrame row by removing currency symbols and commas.

    Args:
        row (pd.Series): A DataFrame row.
        column (str): The name of the column to normalize.

    Returns:
        str: The normalized numeric string, or the original value if it's NaN.
    """
    if not pd.isna(row[column]):
        return normalize_number(row[column])
    else:
        return row[column]




    

# Load the data 
df = pd.read_csv('homework.csv')

# Change date to  ISO 8601
df['system creation date'] = pd.to_datetime(df['system creation date'])

# Change all of the rows for the wholesale column to strings
df['wholesale ($)'] = df['wholesale ($)'].astype(str)

# normalize all of the numbers in the wholesale column
for index, row in df.iterrows():
    df.at[index, 'wholesale ($)'] = normalize_number(row['wholesale ($)'])

# Format the numbers to two decimal places
df['wholesale ($)'] = df['wholesale ($)'].astype(float).map('{:.2f}'.format)

# Map column to strings
df['map ($)'] = df['map ($)'].astype(str)

# Normalize all the nubers in the map column
for index, row in df.iterrows():
    df.at[index, 'map ($)'] = normalize_number(row['map ($)'])
    
# Format the numbers to two decimal places
df['map ($)'] = df['map ($)'].astype(float).map('{:.2f}'.format)


# MSRP column in to strings
df['msrp ($)'] = df['msrp ($)'].astype(str)


# normalize all of the numbers in the MSRP column    
for index, row in df.iterrows():
    df.at[index, 'msrp ($)'] = normalize_number(row['msrp ($)'])

# Formate the numbers
df['map ($)'] = df['map ($)'].astype(float).map('{:.2f}'.format)

# Normalize replacement glass price column
df['replacement glass price ($)'] = df.apply(normalize_value, axis=1, column='replacement glass price ($)')

# Varible for converting cubic feet to cubic inches
cubic_feet_to_inches = 12 ** 3

# Convert all rows to cubic inches for carton 1 column
df['carton 1 volume (cubic feet)'] = df['carton 1 volume (cubic feet)'] * cubic_feet_to_inches

# Rename column to reflect cubic inches
df.rename(columns={'carton 1 volume (cubic feet)': 'carton_1_cubic_inches'}, inplace=True)

# Convert all rows to cubic inches for carton 2 column
df['carton2volumecubicfeet'] = np.where(df['carton2volumecubicfeet'].notna(), df['carton2volumecubicfeet'] * cubic_feet_to_inches, df['carton2volumecubicfeet'])

# Rename column to reflect cubic inches
df.rename(columns={'carton2volumecubicfeet': 'carton_2_cubic_inches'}, inplace=True)

# Rename column to reflect cubic inches
df['carton 3 volume (cubic feet)'] = np.where(df['carton 3 volume (cubic feet)'].notna(), df['carton 3 volume (cubic feet)'] * cubic_feet_to_inches, df['carton 3 volume (cubic feet)'])

# Convert all rows to cubic inches for carton 3 column
df.rename(columns={'carton 3 volume (cubic feet)': 'carton_3_cubic_inches'}, inplace=True)

# UPC column changed into string
df.upc = df.upc.astype(str)

# Create csv of the formatted data
df.to_csv('formatted.csv', index=False)
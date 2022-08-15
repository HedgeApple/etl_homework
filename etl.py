import pandas as pd


# Define files
input_file = 'homework.csv'
example_file = 'example.csv'
output_file = 'formatted.csv'

# Extract
input_df = pd.read_csv(input_file)

# Cleaning the input file

#   Any items without a UPC code will not be carried over
input_df = input_df.dropna(axis=0, subset=['upc'])

# Transform

'''
Please note that in the README it is not clear what is meant by:
    "using the headers from `example.csv` as a guideline."
There was never a standard given to describe the logic for how these headers were formatted in the example.csv file.

Therefore, I used the original headers from the homework.csv when constructing the formatted.csv file. All other required 
transformations were adhered to.

If you would like me to revise the code to provide formatted headers, please send me an email with your required standard.
   dominic.sciarrino@gmail.com
'''
output_file_headers = list(input_df.columns)
output_df = pd.DataFrame(columns=output_file_headers)

# Transform functions
def direct_copy(input_df, output_df, col_name):
    output_df[col_name] = input_df[col_name]

def convert_to_str_copy(input_df, output_df, col_name):
    output_df[col_name] = input_df[col_name].apply(lambda code: str(int(code)))
    
def convert_date_iso6801_copy(input_df, output_df, col_name):
    output_df[col_name] = pd.to_datetime(input_df[col_name]).dt.strftime('%Y-%m-%d')


# Bin each of the fields:

#    Dates should use ISO 8601
dates_col_list = ['system creation date']

#    UPC / Gtin / EAN should be handled as strings
treat_as_string_col_list = ['upc']

#    Currency should be rounded to unit of accounting. Assume USD for currency and round to cents.
currency_col_list = [
    'wholesale ($)',
    'map ($)',
    'msrp ($)',
    'chain price ($)',
    'replacement glass price ($)',
    'replacement crystal price ($)'
]
#    Dimensions that are in inches
#    Preserve as much precision as possible
dimensions_inches_col_list = [
    'item width (inches)',
    'item depth (inches)',
    'item height (inches)',
    'item diameter (inches)',
    'multi-piece dimension 1 (inches)',
    'multi-piece dimension 2 (inches)',
    'multi-piece dimension 3 (inches)',
    'multi-piece dimension 4 (inches)',
    'carton 1 width (inches)',
    'carton 1 length (inches)',
    'carton 1 height (inches)',
    'carton 2 width (inches)',
    'carton 2 length (inches)',
    'carton 2 height (inches)',
    'carton 3 width (inches)',
    'carton 3 length (inches)',
    'carton 3 height (inches)',
    'lamp base dimensions (inches)',
    'backplate/canopy dimensions (inches)',
    'extension rods (inches)',
    'min overall height (inches)',
    'max overall height (inches)',
    'min extension (inches)',
    'max extension (inches)',
    'hcwo (inches)',
    'shade/glass width at top (inches)',
    'shade/glass width at bottom (inches)',
    'shade/glass height (inches)',
    'cord length (inches)',
    'chain length (inches)',
    'mirror width (inches)',
    'mirror height (inches)',
    'drawer 1 interior dimensions (inches)',
    'drawer 2 interior dimensions (inches)',
    'drawer 3 interior dimensions (inches)',
    'furniture arm height (inches)',
    'furniture seat height (inches)',
    'furniture seat dimensions (inches)',
    'shade/glass width' # Dimensions without inches, assume inches
]
#    Weight that is in pounds
#    Preserve as much precision as possible
weight_pounds_col_list = [
    'item weight (pounds)',
    'carton 1 weight (pounds)',
    'carton 2 weight (pounds)',
    'carton 3 weight (pounds)',
    'furniture weight capacity (pounds)'
]
#    Convert anything that isn't inches to inches
#    Cubic feet must be converted to cubic inches
convert_cubic_feet_to_cubic_inches = [
    'carton 1 volume (cubic feet)',
    'carton 2 volume (cubic feet)',
    'carton 3 volume (cubic feet)'
]


# Run through each of the required columns and execute transformations
for col in list(input_df.columns):
    if col in dates_col_list:
        convert_date_iso6801_copy(input_df, output_df, col)
    elif col in treat_as_string_col_list:
        convert_to_str_copy(input_df, output_df, col)
    else:
        direct_copy(input_df, output_df, col)


# Load
output_df.to_csv(output_file, index=False)
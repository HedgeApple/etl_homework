# Define files
input_file = 'homework.csv'
output_file = 'formatted.csv'

# Bin Each Feature

# Dates should use ISO 8601
dates_col_list = ['system creation date']

# UPC / Gtin / EAN should be handled as strings
treat_as_string_col_list = ['upc']

# Currency should be rounded to unit of accounting. Assume USD for currency and round to cents.
currency_col_list = [
    'wholesale ($)',
    'map ($)',
    'msrp ($)',
    'chain price ($)',
    'replacement glass price ($)',
    'replacement crystal price ($)'
]
# Dimensions that are in inches
# Preserve as much precision as possible
dimensions_inches_col_list = [
    'item width (inches)',
    'item depth (inches)',
    'item height (inches)',
    'item diameter (inches)',
    'carton 1 width (inches)',
    'carton 1 length (inches)',
    'carton 1 height (inches)',
    'carton 2 width (inches)',
    'carton 2 length (inches)',
    'carton 2 height (inches)',
    'carton 3 width (inches)',
    'carton 3 length (inches)',
    'carton 3 height (inches)',
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
    'furniture arm height (inches)',
    'furniture seat height (inches)',
    'shade/glass width' # Dimensions without inches, assume inches
]

# Weight that is in pounds
# Preserve as much precision as possible
weight_pounds_col_list = [
    'item weight (pounds)',
    'carton 1 weight (pounds)',
    'carton 2 weight (pounds)',
    'carton 3 weight (pounds)',
    'furniture weight capacity (pounds)'
]
# Convert anything that isn't inches to inches
# Cubic feet must be converted to cubic inches
convert_cubic_feet_to_cubic_inches_list = [
    'carton 1 volume (cubic feet)',
    'carton2volumecubicfeet',
    'carton 3 volume (cubic feet)'
]

converters = {}
converters['upc'] = lambda s: str(s)
for k in dimensions_inches_col_list:
    converters[k] = lambda s: str(s)
for k in weight_pounds_col_list:
    converters[k] = lambda s: str(s)
for k in convert_cubic_feet_to_cubic_inches_list:
    converters[k] = lambda s: str(s)
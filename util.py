import pandas as pd
from globals import *

def direct_copy(input_df, output_df, col_name):
    output_df[col_name] = input_df[col_name]

def convert_to_str_copy(input_df, output_df, col_name):
    output_df[col_name] = input_df[col_name].apply(lambda code: str(int(code)) if code != '' else '')
    
def convert_date_iso6801_copy(input_df, output_df, col_name):
    output_df[col_name] = pd.to_datetime(input_df[col_name]).dt.strftime('%Y-%m-%d')

def format_currency(input_df, output_df, col_name):
    output_df[col_name] = input_df[col_name].apply(lambda s: f"{float(s.replace('$', '').replace(',','')):.2f}" if (type(s) == str) else f"{float(s):.2f}")
    
def format_inches(input_df, output_df, col_name):
    def keep_precision(value_str):
        try:
            before_decimal, after_decimal = value_str.split('.')
        except ValueError as e:
            return ""

        precision = len(after_decimal)
        value = float(value_str)
        return f"{value:.{precision}f}"
    
    output_df[col_name] = input_df[col_name].apply(lambda s: keep_precision(s) if s != 'nan' else "0")

def format_pounds(input_df, output_df, col_name):
    def keep_precision(value_str):
        try:
            before_decimal, after_decimal = value_str.split('.')
        except ValueError as e:
            return ""

        precision = len(after_decimal)
        value = float(value_str)
        return f"{value:.{precision}f}"
    
    output_df[col_name] = input_df[col_name].apply(lambda s: keep_precision(s) if s != 'nan' else "0")

def format_cubic_feet_volume(input_df, output_df, col_name):
    def convert_cubic_feet_to_cubic_inches(i):
        if i == '':
            return ""
        # Conversion factor for cubic feet to cubic inches: 1728
        converted = float(i) * 1728
        return str(converted)
    
    output_df[col_name] = input_df[col_name].apply(lambda s: convert_cubic_feet_to_cubic_inches(s))


#######################################################
#                       Extract                       #
#######################################################

def extract(input, converters):
    return pd.read_csv(input, converters=converters)

#######################################################
#                        Clean                        #
#######################################################

def clean(input_df):
    # Fill NaN in UPC columns with blanks
    input_df['upc'] = input_df['upc'].fillna('')

#######################################################
#                     Transform                       #
#######################################################

def transform(input_df):
    output_df = pd.DataFrame(columns=list(input_df.columns))

    for col in list(input_df.columns):
        if col in dates_col_list:
            convert_date_iso6801_copy(input_df, output_df, col)
        elif col in treat_as_string_col_list:
            convert_to_str_copy(input_df, output_df, col)
        elif col in currency_col_list:
            format_currency(input_df, output_df, col)
        elif col in dimensions_inches_col_list:
            format_inches(input_df, output_df, col)
        elif col in weight_pounds_col_list:
            format_pounds(input_df, output_df, col)
        elif col in convert_cubic_feet_to_cubic_inches_list:
            format_cubic_feet_volume(input_df, output_df, col)
        else:
            direct_copy(input_df, output_df, col)
        
    return output_df
        
#######################################################
#                        Load                         #
#######################################################

def load(export_file_name, df_to_export: pd.DataFrame):
    df_to_export.to_csv(export_file_name, index=False)


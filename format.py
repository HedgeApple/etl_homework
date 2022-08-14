# All modules need to run this file
import csv
import datetime
import re
import pandas as pd
import numpy as np
from numpy import nan
import math

# Created function to reformat CSV data
def csv_format():
    #grabs csv file
    data_frame = pd.read_csv('homework.csv')

    # Gets all header in CSV file and loops through them
    for col in data_frame.columns:

        # Searches for any headers that have UPCs
        if 'upc' in col:

            # In the github page it says all UPCs, Gtins and EANs should be handled as strings
            # So what I got from that is that I need to convert them to a string and nothing else?
            # I looked throught the CSV file and only had one column that had UPCs. No Gtins and EANs..

            # Replaces "Not a number" data types to an empty string
            replace_nan = data_frame[col] = data_frame[col].replace({np.NaN: ''})

            # Gets all upcs and turns them into string datatype
            format_upc = data_frame[col] = data_frame[col].astype(str)

            #print(format_upc,'\n')

            # Saves changes the upcs in location
            data_frame.loc[col, data_frame.columns] = format_upc

        # Searches for any headers that have weight/pounds
        if 'weight' in col:

            # Replaces "Not a number" data types to an empty string
            replace_nan = data_frame[col] = data_frame[col].replace({np.NaN: ''})

            try:
                # It says to convert any unit into pounds nothing more
                # All the values are already in a floating point values
                # so I made sure any weight information are floats and not strings 

                index_pounds = data_frame[col] = data_frame[col].astype(float)
                data_frame.loc[col, data_frame.columns] = index_pounds
            except ValueError:
                pass
            #print(format_pounds)


        if 'dimension' in col: 

            replace_nan = data_frame[col] = data_frame[col].replace({np.NaN: ''})

            index_dimensions = data_frame[col] = data_frame[col].astype(str)

            #print(format_inches,'\n')

            data_frame.loc[col, data_frame.columns] = index_dimensions


        if 'inches' in col:

            replace_nan = data_frame[col] = data_frame[col].replace({np.NaN: ''})
            try:
                index_inches = data_frame[col] = data_frame[col].astype(float)
                data_frame.loc[col, data_frame.columns] = index_inches
            except ValueError:
                pass

            #print(format_inches,'\n')

            #data_frame.loc[col, data_frame.columns] = index_inches

        if 'date' in col:

            date_format = data_frame[col] = data_frame[col]

            # Changed all dates to the ISO 8601 standard from d/m/yyyy to yyyy/m/d
            # using the datetime module

            new_date_format = data_frame[col] = pd.to_datetime(
            data_frame[col]).dt.strftime('%Y/%m/%d')

            #print(new_date_format,'\n')

            data_frame.loc[col, data_frame.columns] = new_date_format



    #iterates through data in data frame
    for index, row in data_frame.iterrows():


        # Changes all prices to strings.
        # Gets rid of any chracter not a integer, comma or decimal.
        # Turns the prices to floats.
        # Then rounds the floats.
        # Then changes prices to the correct price format.


        whole_sale = str(row['wholesale ($)'])
        whole_sale = re.sub('[^0-9,.]', '', whole_sale)


        map_price = str(row['map ($)'])
        map_price = re.sub('[^0-9,.]', '', map_price)


        try:
            whole_sale = float(whole_sale)
            whole_sale_round = round(whole_sale)
            whole_sale_format = '${:0>3}'.format('{:,.2f}'.format(whole_sale_round))


            map_price = float(map_price)
            map_price_round = round(map_price)
            map_price_format = '${:0>3}'.format('{:,.2f}'.format(map_price_round))


            data_frame.loc[index, 'wholesale ($)'] = whole_sale_format
            data_frame.loc[index, 'map ($)'] = map_price_format
        except ValueError:
            pass

         
    # Saves updated data in the format csv
    data_frame.to_csv('formatted.csv', index = False)    

if __name__ == '__main__':
    csv_format()
# Import libraries
import pandas as pd
import json 
from aux_funcs import date_to_iso, get_size

# Import dictionary from json file in order to filter and rename some columns later on (this could have been done with a Python dictionary directly but since this is not an .ipynb file the dictionary cannot be 'hidden' and therefore it's cleaner not to have it in the middle of the code)
with open("dict.json", encoding="utf-8-sig") as f:
    dictionary:dict = json.load(f)

# Read DataFrames from .csv files
df_hw:pd.DataFrame = pd.read_csv("./homework.csv")
df_ex:pd.DataFrame = pd.read_csv("./example.csv")

# UPC column transformation (hyphens were added when necessary)
df_hw["upc"] = df_hw["upc"].astype(str).apply(lambda x: x[:3] + "-" + x[3:-3] + "-" + x[-3:-2])

# Country of origin column transformation (replaced names with abbreviation)
df_hw["country of origin"].replace(dictionary["Countries"], inplace=True)

# Item style column transformation (all styles columns were combined. If there was more than one value in a cell (separated by a "/") the first value was left. Before concatenating cells ", " and " & " were added to item substyles columns in order to get the desired format)
style_columns:list =  ["item style", "item substyle", "item substyle 2"]

df_hw.loc[df_hw["item substyle"].notna(), "item substyle"] = df_hw.loc[df_hw["item substyle"].notna(), "item substyle"].apply(lambda x: ", " + str(x).strip())
df_hw.loc[df_hw["item substyle 2"].notna(), "item substyle 2"] = df_hw.loc[df_hw["item substyle 2"].notna(), "item substyle 2"].apply(lambda x: " & " + str(x).strip())

for column in style_columns:
    df_hw[column].fillna("",inplace = True)
    filter = df_hw[column].str.count("/") > 0
    df_hw.loc[filter, column] = df_hw.loc[filter, column].str.split("/").str[0]  # If there is a "/" in the cell, leave only the first value after splitting
df_hw["item style"] = df_hw["item style"].str.strip() + df_hw["item substyle"] + df_hw["item substyle 2"]

# Create Product size column out of title and description (Text Mining)
df_hw["item size"] = df_hw["description"].apply(lambda x: get_size(x))
df_hw.loc[df_hw["item size"].isna(), "item size"] = df_hw.loc[df_hw["item size"].isna(), "long description"].apply(lambda x: get_size(x))

# NOTE: The following two transformations won't be seen in the final DataFrame because the columns are not included in the headers list of example.csv, they were done just to illustrate how the process would look in case of needing it
# System Creation Date Column transformation
df_hw["system creation date"] = df_hw["system creation date"].apply(lambda x: date_to_iso(x))
# MSRP($) Column transformation (the same process could be done with map and wholesale price)
df_hw["msrp ($)"] = df_hw["msrp ($)"].apply(lambda x: round(float(str(x).replace("$", "").replace(",","").strip()),2)) 


# Rename all the columns that are included in the headers list of example.csv
new_columns:list = [dictionary["Columns"][column] if column in dictionary["Columns"] else column for column in df_hw.columns]
df_hw.columns:pd.Index = new_columns

# Drop columns that are not in example.csv
columns_to_drop:list = [column for column in df_hw.columns if column not in list(dictionary["Columns"].values())]
df_hw.drop(columns_to_drop, inplace = True, axis = 1)

# Add the remaining unmatched columns of example.csv, that will be left empty 
columns_to_add:list = [column for column in df_ex.columns if column not in df_hw.columns]
for column_to_add in columns_to_add:
    df_hw[column_to_add] = ""
    
# Export to .csv file 
df_hw.to_csv("formatted.csv", index=False)
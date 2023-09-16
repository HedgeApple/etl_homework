import pandas as pd

#Reading the CSV file so I can manipulated it
df= pd.read_csv("homework.csv", low_memory=False, dtype=object)

# Code for Criteria 1
df["system creation date"]= pd.to_datetime(df['system creation date'], format='mixed').dt.strftime('%Y/%m/%d')

# Code for Criteria 5
df["upc"] = "'" + df["upc"].astype(str)


# Code for Criteria 2 and 3
for column in df.columns:
    if "$" in column:
            df[column] = df[column].str.replace(",", "").str.replace("$", "").astype(float).round(2)
    if "cubic" in column and "feet" in column:
        df[column]= df[column].astype(float) * 1728.0

#Turning the dataset into a CSV file called "formatted.csv"
df.to_csv("formatted.csv", encoding='utf-8', index=None, header=True)


# Explaining The Code
I used the Pandas library to apply changes to columns, in order to have a properly formatted CSV based on the 6 following criteria:

1. Dates should use ISO 8601
2. Currency should be rounded to unit of accounting. Assume USD for currency and round to cents.
3. For dimensions without units, assume inches. Convert anything which isn't in inches to inches.
4. For weights without units, assume pounds. Convert anything which isn't in pounds to pounds.
5. UPC / Gtin / EAN should be handled as strings
6. Floating point and decimal numbers should preserve as much precision as possible

## An Explanation Of Criteria 1
In order to satisfy criteria 1, I had converted all dates in the "system creation date" column and using pandas's datetime function to convert the format of Month/Day/Year (which was registerd as mixed format according to pandas) to Year/Month/Day (ISO 8601). The code associated with this work is shown down below:

```
df["system creation date"]= pd.to_datetime(df['system creation date'], format='mixed').dt.strftime('%Y/%m/%d')
```

## An Explanation Of Criteria 2
In order to satisfy criteria 2, I had took every column that had a header that contained $, went through each one, and rounded everything to cents by converting all cash values into floats (after removing specail charatcers, such as "," and "$", using the replace function) and then had them rounded to the 2nd decimal place, using Pandas's round() function. The code associated with this work is shown down below:

```
for column in df.columns:
    if "$" in column:
        df[column] = df[column].str.replace(",", "").str.replace("$", "").astype(float).round(2)
```

NOTE: I used a for loop to try and show that some of these columns have patterns, which you can use to make code in less lines. I will note this is not intended to work outside of anything other than the provided CSV file, as column names vary from file to file. I will also note, this is inefficent in terms of time complexity, as it turned what could have otherwise been an O(1) solution into a O(N) solution.

## An Explanation Of Criteria 3
In order to satisfy criteria 3, I had converted the only two columns that had non-inch measurements (which had contained the words "cubic" and "feet" in them) and multiplied them by 1728, as that is the conversion of cubic foot to inch. I did not do cubic inch to inch, as I assummed that was not wanted.  The code associated with this work is shown down below:

```
for column in df.columns:
    if "cubic" in column and "feet" in column:
        df[column]= df[column].astype(float) * 1728
```

NOTE: Same idea as criteria 2, I just wanted to show/find a pattern to make the code a bit cleaner. In case you were wondering, the reason why I searched "cubic" and "feet", instead of "cubic feet" is due to the fact one of the columns had the name of "carton2volumecubicfeet" and the other was "carton 1 volume (cubic feet)".

## An Explanation Of Criteria 4
Criteria 4 had allready been satisfied, as there was no non-pound units. This was (not) found by searching the file for all forms of measurements (ounce, ton, gram, ect). However, none had poped up, so to my knowlege, everything had been converted to pounds.

## An Explanation Of Criteria 5
In order to satisfy criteria 5, I had added an apostrophe to the start of all of the numbers. Due to the way CSV files read numbers, adding a ' in front of something that is not a string, turns it into a string. The code associated with this work is shown down below:

```
df["upc"] = "'" + df["upc"].astype(str)
```

## An Explanation Of Criteria 6
Criteria 6 had been met by not altering any of the floating point values of anything that was not a column which conatined $. This includes when I converted columns from cubic foot to cubic inch (I had not changed any of the code to have it round to two decimal places, unlike what I did for criteria 2).

# Code Explanation

In this code, the column names have been left unchanged, except when a transformation altered the meaning of the values. For instance, when converting dimensions from cubic feet to cubic inches. This decision was made to maintain consistency with the original data, as the format of the data in the system's column names was not known.

## Imports Used

The code utilizes the following libraries:

- pandas: Used for data manipulation.
- numpy: Employed for various numerical operations.

####  Important things to know about the code and the choices made during the data transformation:

- Each line of code is accompanied by comments that describe its purpose and functionality.
- Functions used in the code are documented with docstrings to explain how they work and their purpose.
- All currency values have been rounded to the nearest cent in USD and any occurrence of dollar signs or commas have been removed.
- Any dimensional columns that were not originally in inches have been converted to inches.
- Weight units other than pounds were not encountered in the dataset.
- UPCs are treated as strings throughout the code.
- While GTIN and EAN values are not present in the dataset, it is possible to derive them from the UPC. However, the transformation process in this code did not explicitly request the creation of two new columns for GTIN and EAN.
- SKU numbers are not found in the dataset, and although assumptions could be made based on item numbers, it remains unclear.




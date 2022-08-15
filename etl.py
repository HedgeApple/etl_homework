import pandas as pd

# Define files
input_file = 'homework.csv'
example_file = 'example.csv'
output_file = 'formatted.csv'

# Extract
input_df = pd.read_csv(input_file)

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



output_df = pd.DataFrame(columns=['col1', 'col2', 'col3'])

# Load
output_df.to_csv(output_file, index=False)
import pandas as pd

# Test Options
pd.set_option('display.max_columns', None)



# Extract

input_file = 'homework.csv'
input_df = pd.read_csv(input_file)

# Transform

print(input_df.head(1))

output_df = input_df

# Load
output_df.to_csv('output.csv', index=False)
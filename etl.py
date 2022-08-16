from globals import *
from util import *

# Extract
input_df = extract(input_file, converters)
clean(input_df)

# Transform
output_df = transform(input_df)

# Load
load(output_file, output_df)
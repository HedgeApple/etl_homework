#### ETL assignment submission.

This script mainly uses `pandas` library for parsing/altering data on input file. `ETL` class is defined as an entry point for the script. Class has `process_data` `classmethod` which will perform the transform operation. Input file is loaded by.

#### Example workflow :rocket:
- `process_data` takes in argument `dataframe` which is a `pandas.DataFrame` object and `output_filename` for the result file.
- A `dict` object is defined within `ETL` class which maps column names to new column names.
- Method iterates through key, value pairs of column name mapping.
- For each key, `get_transformer_for_column` method is called to get a helper `transformer` function which will alter the given data into expected format such as `date`, `bool`, `upc`...
- Pandas `apply` method will perform transforms on each cell under given column and transformed data will be written into a new file.
- Output file will be generated in the same directory.

## Requirements

- pandas

- tqdm (for progress bar)

## Running script
- (Optional) Create a virtual environment
	```bash
	python -m virtualenv .venv
	# Activate
	source .venv/bin/activate
	# Or windows
	.venv/Scripts/activate
- Install dependencies
	```bash
	pip install -r requirements.txt
	```
- Run the script
	 ```bash
	 python main.py
   ```
   This will generate output csv file which is named as `formatted` by default
		
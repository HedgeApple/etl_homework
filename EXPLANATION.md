# Code structure

Almost all the code is written in the `main.py` file, which serves as the execution point. There's also a  `aux_funcs.py`  file where I wrote the auxiliary functions. In adittion, I utilized a `dict.json` to store useful data, such as the columns that should be renamed from the `homework.csv` file based on the headers in `example.csv`.

# How it works

The script reads in `homework.csv` as a DataFrame and transforms several columns (and its values) based on `example.csv`. 

*For instance: UPC, Item style, Item size, country of origin.*

After having modified these, it renames all the columns I was able to track, and adds the ones that are missing as empty columns.


***Note:***

*Due to the lack of information I wasn't able to match some columns. For example, I couldn't create the metric 'min_price' or 'cost_price'*

*out of 'wholesale price' and 'map price'.*

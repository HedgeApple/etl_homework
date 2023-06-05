# Import libraries
import pandas as pd
from datetime import datetime

def date_to_iso(date_string:str) -> str:
    """
    Function that transforms date into ISO 8601
    """
    date:str = datetime.strptime(date_string, "%m/%d/%Y")
    return date.strftime("%Y-%m-%d")


def get_size(text:str) -> str: # Note that it could have been used an if/elif for each case because there are only three types, but this way is shorter
    """
    Function that gets a size if it is mentioned inside a text
    """
    sizes:list = ["small", "medium", "large"]
    for term in sizes:
        if pd.isna(text):
            return None
        elif term in text.lower():
            return term.capitalize()
        else:
            continue

  
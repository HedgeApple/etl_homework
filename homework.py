import csv
# From my understanding basically a module or library in python.
# DictReader class operates like a regular reader but maps the information read into a dictionary. The keys for the dictionary can be passed in with the fieldnames parameter or inferred from the first row of the CSV file.
# Dictionaries are data types in Python which allows us to store data in key/value pair. Similar to objects in JS.
from csv import DictReader
# File handling is an integral part of programming. File handling in Python is simplified with built-in methods, which include creating, opening, and closing files. While files are open, Python additionally allows performing various file operations, such as reading, writing, and appending information.
#"r" stands for read
file_handle = open("data/manufacture.csv", "r", encoding="utf8")
csv_reader = DictReader(file_handle)

with open('formatted.csv', 'w', encoding="utf8") as csvfile:
    writer = csv.DictWriter(csvfile, csv_reader.fieldnames)
    writer.writeheader()
    writer.writerows(csv_reader)
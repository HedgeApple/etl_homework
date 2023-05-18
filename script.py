# importing csv library to read and write from and to csv file
import csv

header_values = []
# Open the example.csv file and read the file data
with open('example.csv', 'r') as file_example:
    example_csv = csv.reader(file_example)
    header_values = next(example_csv)

with open('homework.csv', 'r') as file_input:
    homework_csv = csv.reader(file_input)
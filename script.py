import csv

rows = []
header = []
formatted_rows = []

with open("homework.csv", "r") as homework_file:
    hw_rows = csv.reader(homework_file)
    hw_header = next(hw_rows)

    for row in hw_rows:
        rows.append(row)

with open("example.csv", "r") as example_file:
    ex_rows = csv.reader(example_file)
    ex_header = next(ex_rows)

for hw_cell in hw_header:
    for ex_cell in ex_header:
        if ex_cell in hw_cell:
            header.append(hw_cell)
        elif hw_cell == "description" and hw_cell not in header:
            header.append(hw_cell)
        elif hw_cell == "item number" and hw_cell not in header:
            header.append(hw_cell)
        elif hw_cell == "upc" and hw_cell not in header:
            header.append(hw_cell)
        elif "$" in hw_cell and hw_cell not in header:
            header.append(hw_cell)

for row in rows:
    temp_row = []
    for el in row:
        for col in header:
            if row.index(el) == hw_header.index(col):
                temp_row.append(el)
    formatted_rows.append(temp_row)
    temp_row = []

formatted = open('formatted.csv', 'w')
writer = csv.writer(formatted)
writer.writerow(header)
for row in formatted_rows:
    writer.writerow(row)

import csv
import datetime

# Define the conversion factors for units
unit_conversions = {
    "inches": 1,
    "ft": 12,
    "cm": 0.393701,
    "mm": 0.0393701,
    "yd": 36,
    "m": 39.3701,
    "pounds": 1,
    "kg": 2.20462,
    "g": 0.00220462
}

# Open homework.csv and example.csv files
with open('homework.csv', 'r') as homework_file, open('example.csv', 'r') as example_file:
    # Create a CSV reader for each file
    homework_reader = csv.reader(homework_file)
    example_reader = csv.reader(example_file)
    
    # Get the header row from each file
    homework_header = next(homework_reader)
    example_header = next(example_reader)
    
    # Create a new list to store the data
    data = []
    
    # Iterate through the rows in the homework file
    for row in homework_reader:
        # Get the item name, price, UPC_Gtin_EAN, date, dimension, weight
        item_name = row[0]
        price = row[1]
        UPC_Gtin_EAN = row[2]
        date = row[3]
        dimension = row[4]
        weight = row[5]
        
        # Check if price is a valid float
        try:
            float(price)
        except ValueError:
            # Handle as a string
            price = price
        else:
            price = round(float(price), 2)
        
        # Check if UPC/Gtin/EAN is valid integer
        try:
            int(UPC_Gtin_EAN)
        except ValueError:
            # Handle as a string
            UPC_Gtin_EAN = UPC_Gtin_EAN
        else:
            UPC_Gtin_EAN = int(UPC_Gtin_EAN)
        
        # Transform the date to ISO 8601 format
        try:
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
            date = date.isoformat()
        except ValueError:
            pass
        
        # Convert the dimensions to inches
        try:
            if dimension[-2:] in unit_conversions:
                unit = dimension[-2:]
                value = float(dimension[:-2])
                dimension = round(value * unit_conversions[unit], 4)
            else:
                dimension = round(float(dimension), 4)
        except ValueError:
            pass
        
        # Convert the weight to pounds
        try:
            if weight[-2:] in unit_conversions:
                unit = weight[-2:]
                value = float(weight[:-2])
                weight = round(value * unit_conversions[unit], 4)
            else:
                weight = round(float(weight), 4)
        except ValueError:
            pass
        # Append the item name, price, UPC_Gtin_EAN, date, dimension, weight to the data list
        data.append([item_name, price, UPC_Gtin_EAN, date, dimension, weight])
    
    # Iterate through the rows in the example file
    for row in example_reader:
        # Get the item name, price, UPC_Gtin_EAN, date, dimension, weight
        item_name = row[0]
        price = row[1]
        UPC_Gtin_EAN = row[2]
        date = row[3]
        dimension = row[4]
        weight = row[5]
        
        # Check if price is a valid float
        try:
            float(price)
        except ValueError:
            # Handle as a string
            price = price
        else:
            price = round(float(price), 2)
        
        # Check if UPC/Gtin/EAN is valid integer
        try:
            int(UPC_Gtin_EAN)
        except ValueError:
            # Handle as a string
            UPC_Gtin_EAN = UPC_Gtin_EAN
        else:
            UPC_Gtin_EAN = int(UPC_Gtin_EAN)
        
        # Transform the date to ISO 8601 format
        try:
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
            date = date.isoformat()
        except ValueError:
            pass
        
        # Convert the dimensions to inches
        try:
            if dimension[-2:] in unit_conversions:
                unit = dimension[-2:]
                value = float(dimension[:-2])
                dimension = round(value * unit_conversions[unit], 4)
            else:
                dimension = round(float(dimension), 4)
        except ValueError:
            pass
        
        # Convert the weight to pounds
        try:
            if weight[-2:] in unit_conversions:
                unit = weight[-2:]
                value = float(weight[:-2])
                weight = round(value * unit_conversions[unit], 4)
            else:
                weight = round(float(weight), 4)
        except ValueError:
            pass
        
        # Append the item name, price, UPC_Gtin_EAN, date, dimension, weight to the data list
        data.append([item_name, price, UPC_Gtin_EAN, date, dimension, weight])

    # Open a new file named 'formatted.csv' in write mode
    with open('formatted.csv', 'w', newline='') as formatted_file:
        # Create a CSV writer object
        writer = csv.writer(formatted_file)

        # Write the header row to the new file
        writer.writerow(['Item Name', 'Price', 'UPC/Gtin/EAN', 'Date', 'Dimension', 'Weight'])

        # Write the data to the new file
        writer.writerows(data)


import csv
import datetime

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
        # Get the item name and price
        item_name = row[0]
        price = row[1]
        UPC_Gtin_EAN = row[2]
        
        # Check if price is a valid float
        try:
            float(price)
        except ValueError:
            # Handle as a string
            price = price
        else:
            price = float(price)
        
        # Check if UPC/Gtin/EAN is valid integer
        try:
            int(UPC_Gtin_EAN)
        except ValueError:
            # Handle as a string
            UPC_Gtin_EAN = UPC_Gtin_EAN
        else:
            UPC_Gtin_EAN = int(UPC_Gtin_EAN)
        
    
        
        # Append the item name, formatted price, and UPC_Gtin_EAN to the data list
        data.append([item_name, price,UPC_Gtin_EAN])
    
    # Iterate through the rows in the example file
    for row in example_reader:
        # Get the item name and price
        item_name = row[0]
        price = row[1]
        UPC_Gtin_EAN = row[2]
        
        # Check if price is a valid float
        try:
            float(price)
        except ValueError:
            # Handle as a string
            price = price
        else:
            price = float(price)
        
        # Check if UPC/Gtin/EAN is valid integer
        try:
            int(UPC_Gtin_EAN)
        except ValueError:
            # Handle as a string
            UPC_Gtin_EAN = UPC_Gtin_EAN
        else:
            UPC_Gtin_EAN = int(UPC_Gtin_EAN)
        
   
        # Append the item name, formatted price, and UPC_Gtin_EAN to the data list
        data.append([item_name, price,UPC_Gtin_EAN])

# Open a new file named 'formatted.csv' in write mode
with open('formatted.csv', 'w', newline='') as formatted_file:
    # Create a CSV writer object
    writer = csv.writer(formatted_file)
    
    # Write the header row to the new file
    writer.writerow(['Item Name', 'Price', 'UPC/Gtin/EAN'])
    
    # Write the data to the new file
    writer.writerows(data)

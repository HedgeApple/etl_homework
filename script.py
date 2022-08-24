


import pandas as pd  # Include pandas in requirements.txt
import pycountry

def format_csv():
    
    # Pandas formatting to display decimal places
    pd.options.display.float_format = '{:,.3f}'.format

    # The explicit columns we want to use from homework.csv
    spec_columns = [r'item number', r'upc', r'item weight (pounds)',
    r'item depth (inches)', r'item width (inches)',
    r'item height (inches)', r'url california label (pdf)', 
    r'wholesale ($)', r'map ($)', r'min order qty', r'item category', r'brand',
    r'description', r'long description', r'selling point 1', r'selling point 2', r'selling point 3',
    r'selling point 4', r'selling point 5', r'selling point 6', r'selling point 7', r'country of origin',
    r'furniture arm height (inches)', r'bulb 1 included', r'bulb 1 type', r'primary color family', r'cord length (inches)', r'item finish',
    r'switch type', r'item materials', r'bulb 1 count', r'outdoor', r'furniture seat height (inches)', r'shade/glass description', r'bulb 1 wattage',
    r'carton 1 weight (pounds)', r'carton 1 length (inches)', r'carton 1 height (inches)', r'carton 1 width (inches)',
    r'carton 2 weight (pounds)', r'carton 2 length (inches)', r'carton 2 height (inches)', r'carton 2 width (inches)',
    r'carton 3 weight (pounds)', r'carton 3 length (inches)', r'carton 3 height (inches)', r'carton 3 width (inches)', r'item style']

    # Columns we use to create the item description
    desc_columns = [r'item materials', r'item finish', r'item finish 1', r'item finish 2', r'item finish 3', r'item collection', r'item substyle', r'item substyle 2', r'bulb 2 count']

    # Read homework.csv using only the specified columns above. low_memory=False to handle a flag attributed to multiple dtypes in the dataframe
    specs = pd.read_csv("homework.csv", usecols=spec_columns, low_memory=False)

    # Reindex our dataframe according to our spec_columns list, which was ordered in relation to example.csv
    specs = specs.reindex(columns=spec_columns)

    # Insert a couple new columns we will need (these columns reference columns already read from homework.csv, and you cant read a column twice so we add these manually)
    specs.insert(27, "attrib__distressed_finish", " ") # Will be used for the disstressed finish column
    specs.insert(35, "switch type2", " ") # Will be used for the switch type column

    # Re-read homework.csv using columns relating to descriptions, for us to create our product descriptions, and our product styles
    descriptions = pd.read_csv("homework.csv", usecols=desc_columns, low_memory=False)

    # Columns we want to 
    example_columns = [r'manufacturer_sku', r'ean13', r'weight', r'length', r'width', r'height', r'prop_65', r'cost_price', r'min_price', r'made_to_order',
    r'product__product_class__name', r'product__brand__name', r'product__title', r'product__description', r'product__bullets__0', r'product__bullets__1', r'product__bullets__2',
    r'product__bullets__3', r'product__bullets__4', r'product__bullets__5', r'product__bullets__6', r'product__country_of_origin__alpha_3', r'attrib__arm_height', r'attrib__bulb_included',
    r'attrib__bulb_type', r'attrib__color', r'attrib__cord_length', r'attrib__distressed_finish', r'attrib__finish', r'attrib__hardwire', r'attrib__material', r'attrib__number_bulbs',
    r'attrib__outdoor_safe', r'attrib__seat_height', r'attrib__shade', r'attrib__switch_type', r'attrib__wattage', r'boxes__0__weight', r'boxes__0__length',
    r'boxes__0__height', r'boxes__0__width', r'boxes__1__weight', r'boxes__1__length', r'boxes__1__height', r'boxes__1__width', r'boxes__2__weight', r'boxes__2__length',
    r'boxes__2__height', r'boxes__2__width', r'product__styles']

    # Get a list of our headers from our 'specs' dataframe
    # (cannot use our list 'spec_columns', because we added columns to the dataframe after reading the csv)
    specs_header = list(specs.columns)

    # Create dictionary of our homework.csv (with new columns inserted) headers as keys, and example.csv headers as values (this is used for renaming the headers later)
    new_header = {}
    for old in specs_header:
        for new in example_columns:
            new_header[old] = new
            example_columns.remove(new)
            break

    # CONVERT UPC TO EAN-13
    specs['upc'] = specs['upc'].apply(str)  # Convert column from float to string
    counter = 0
    for i in specs['upc']:
        i = '0' + i  # Adding 0 to the beginning of the string
        i = i[:-2]  # Removing the last 2 characters ('.' and '0' because this column is read as a float initially)
        specs.loc[counter, 'upc'] = i[:3] + '-' + i[3:-1] + '-' + i[-1:]  # Splitting the string and adding hyphens in the appropriate places
        counter += 1

    
    # FORMATTING COST_PRICE (wholesale ($))
    counter = 0
    for i in specs['wholesale ($)']:

        # Remove '$' from any cells
        if "$" in str(i):
            try:
                specs.loc[counter, "wholesale ($)"] = specs.loc[counter, "wholesale ($)"].replace("$", "")  # Remove '$' if it appears in the string, otherwise ignore
            except:
                continue
            
            # Remove ',' from any cells
            if "," in str(i):
                try:
                    specs.loc[counter, "wholesale ($)"] = specs.loc[counter, "wholesale ($)"].replace(",", "")  # Remove ',' if it appears in the string, otherwise ignore
                except:
                    continue
            counter += 1
        else:
            counter += 1

    # Convert column dtype to float values
    specs['wholesale ($)'] = specs['wholesale ($)'].apply(float)

    # Format floats to contain 2 decimal places
    specs["wholesale ($)"] = specs["wholesale ($)"].apply(lambda x: "{:.2f}".format (x))

    # FORMATTING MIN_PRICE (map ($)) COLUMN
    counter = 0
    for i in specs['map ($)']:

        # Remove '$' from any cells
        if "$" in str(i):
            try:
                specs.loc[counter, "map ($)"] = specs.loc[counter, "map ($)"].replace("$", "")  # Remove '$' if it appears in the string, otherwise ignore
            except:
                continue

            # Remove ',' from any cells
            if "," in str(i):
                try:
                    specs.loc[counter, "map ($)"] = specs.loc[counter, "map ($)"].replace(",", "")  # Remove ',' if it appears in the string, otherwise ignore
                except:
                    continue
            counter += 1
        else:
            counter += 1

    # Convert column dtype to float
    specs["map ($)"] = specs["map ($)"].apply(float)

    # Format floats to contain 2 decimal places
    specs["map ($)"] = specs["map ($)"].apply(lambda x: "{:.2f}".format (x))


    # PROP_65 COLUMN (read california label column, if a value is present, assume it to be a link to the prop 65 label, mark it True)
    counter = 0
    for i in specs['url california label (pdf)']:
        if i:
            specs.loc[counter, 'url california label (pdf)'] = "True"
        else:
            specs.loc[counter, 'url california label (pdf)'] = "False"
        counter += 1

    # MADE TO ORDER (not sure exactly which values correspond to this, so just using 'min order qty' and if its greater than 1, say its made to order)
    counter = 0
    for i in specs['min order qty']:
        if int(i) > 1:
            specs.loc[counter, 'min order qty'] = "True"
        elif int(i) <= 1:
            specs.loc[counter, 'min order qty'] = "False"

        counter += 1

    # PRODUCT DESCRIPTION (create dynamic descriptions that are based on 'item finish', 'item material', and 'description' columns)
    # Only adds finishes and materials to the new description if they are not already part of the existing description, to avoid repetition
    counter = 0
    for x in descriptions['item finish']:
        new_desc = specs.loc[counter, 'description'] # Take description of item as our base
        finish = ""
        materials = ""

        # Split 'item finish' into list, iterate through list, if the finish is not a part of the description, concatenate it to 'finish'
        for i in str(descriptions.loc[counter, 'item finish']).split(", "):
            if type(i) == str:
                if i == 'nan':
                    pass
                else:
                    if i not in specs.loc[counter, 'description']:

                        # If the 'finish' variable is empty, dont add ' and ' as this will be the first finish
                        if len(finish) > 1:
                            finish = i + ' and ' + finish
                        else:
                            finish = i

        # Same method used for finishes, check for materials already being listed in the description
        for i in str(descriptions.loc[counter, 'item materials']).split(", "):
            if type(i) == str:
                if i == 'nan':
                    pass
                else:
                    if i not in specs.loc[counter, 'description']:

                        # If the 'materials' variable is empty, dont add ' and ' as this will be the first material
                        if len(materials) > 1:
                            materials = i + ' and ' + materials
                        else:
                            materials = i

        # Concatenate variables 'finish' and 'materials' to the item name to form our new description of the item
        if len(finish) > 1:
            new_desc = 'a ' + finish + ' ' + new_desc
            if len(materials) > 1:
                new_desc = new_desc + ' made of ' + materials
            elif len(materials) == 0:
                pass
        elif len(finish) == 0:
            if len(materials) > 1:
                new_desc = 'a ' + new_desc + ' made of ' + materials
            elif len(materials) == 0:
                new_desc = 'a ' + new_desc

        specs.loc[counter, 'long description'] = new_desc.lower()
        counter += 1

    # Country of origin column
    counter = 0

    for i in specs['country of origin'].apply(str):
        if i == 'nan':
            specs.loc[counter, 'country of origin'] = ''
        else:

            # Philippines spelled incorrectly in homework.csv
            if i == 'Phillipines':
                i = pycountry.countries.get(name = 'Philippines')
                specs.loc[counter, 'country of origin'] = i.alpha_3

            # Vietnam is recognized as 'Viet Nam' when referring to ISO 3166
            elif i == 'Vietnam':
                i = pycountry.countries.get(name = 'Viet Nam')
                specs.loc[counter, 'country of origin'] = i.alpha_3

            else:
                i = pycountry.countries.get(name = str(i))
                specs.loc[counter, 'country of origin'] = i.alpha_3
        counter += 1

    # ATTRIB__DISTRESSED_FINISH / ATTRIB__FINISH
    counter = 0
    for i in descriptions['item finish'].apply(str):
        if 'distressed' in i.lower():
            specs.loc[counter, 'attrib__distressed_finish'] = 'True'
        else:
            specs.loc[counter, 'attrib__distressed_finish'] = 'False'
        counter += 1

    # ATTRIB__NUMBER_BULBS
    counter = 0
    for i in specs['bulb 1 count']:
        if str(i) == 'nan':
            if str(descriptions.loc[counter, 'bulb 2 count']) == 'nan':
                pass
            else:
                specs.loc[counter, 'bulb 1 count'] = int(descriptions.loc[counter, 'bulb 2 count'])
        else:
            if str(descriptions.loc[counter, 'bulb 2 count']) == 'nan':
                pass
            else:
                specs.loc[counter, 'bulb 1 count'] = int(i) + int(descriptions.loc[counter, 'bulb 2 count'])

    # ATTRIB__SWITCH_TYPE
    counter = 0
    for i in specs['switch type'].apply(str):
        if i == 'nan':
            specs.loc[counter, 'switch type2'] = ''
        else:
            specs.loc[counter, 'switch type2'] = i
        counter += 1

    # ATTRIB__HARDWIRE
    # If switch type is listed, consider it hardwired
    counter = 0
    for i in specs['switch type'].apply(str):
        if i == 'nan':
            specs.loc[counter, 'switch type'] = "False"
        else:
            specs.loc[counter, 'switch type'] = "True"
        counter += 1

    # PRODUCT__STYLES
    # Concatenate 'item style' with 'item substyle' and 'item substyle 2'
    counter = 0
    for i in specs['item style'].apply(str):
        if str(descriptions.loc[counter, 'item substyle']) != 'nan':
            if str(descriptions.loc[counter, 'item substyle 2']) != 'nan':
                specs.loc[counter, 'item style'] = i + ', ' + str(descriptions.loc[counter, 'item substyle']) + ', ' + str(descriptions.loc[counter, 'item substyle 2'])
            else:
                specs.loc[counter, 'item style'] = i + ', ' + str(descriptions.loc[counter, 'item substyle'])
        elif str(descriptions.loc[counter, 'item substyle 2']) != 'nan':
            specs.loc[counter, 'item style'] = i + ', ' + str(descriptions.loc[counter, 'item substyle 2'])
        else:
            pass
        counter += 1

    # Rename our header columns to match example.csv, save to 'formatted.csv'
    specs.rename(columns=new_header, inplace=True)
    specs.to_csv("formatted.csv", index=False)


format_csv()

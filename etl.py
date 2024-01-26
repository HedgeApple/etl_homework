from datetime import datetime
import csv

# #Transforms date to ISO 8601 format
# def format_date(date_str):
#     date_obj = datetime.strptime(date_str, '%m/%d/%Y')
#     return date_obj.strftime('%Y-%m-%d')

# def convert_to_in(dimensions):
#     value, unit = dimensions.split(' ')
#     value = float(value)
    
#     if unit.lower() == 'cm':
#         value /= 2.54
    
#     return round(value, 2)

# def convert_to_lbs(weight):
#     value, unit = weight.split(' ')
#     value = float(value)
    
#     if unit.lower() == 'kg':
#         value *= 2.205 
    
#     return round(value, 2)

def format_currency(currency):
    if currency == '':
        return "0.00"
    if currency[0] == '$':
        currency = currency[1:]
    currency = currency.replace(",", "")
    return f"{round(float(currency), 2):.2f}"

def convert_UPC_to_EAN13(UPC):
    EAN13 = '0' + UPC
    EAN13 = EAN13[:3] + '-' + EAN13[3:11] + '-' + EAN13[12:]
    return EAN13

def transform_data(input_header, input_data, output_header):
    input_items = []
    for i, row in enumerate(input_data):
        input_items.append({})
        for j, header in enumerate(input_header):
            input_items[i][header] = row[j]

    output_items = []
    for input_row in input_items:
        output_row = {}

        output_row['manufacturer_sku'] = input_row['item number']
        output_row['ean13'] = convert_UPC_to_EAN13(input_row["upc"])
        output_row['weight'] = input_row["item weight (pounds)"]
        output_row['length'] = input_row["item depth (inches)"]
        output_row['width'] = input_row["item width (inches)"]
        output_row['height'] = input_row["item height (inches)"]
        output_row['prop_65'] = "" 
        output_row['cost_price'] = format_currency(input_row["wholesale ($)"])
        output_row['min_price'] = format_currency(input_row["map ($)"])
        output_row['made_to_order'] = ""
        output_row['product__product_class__name'] = input_row["item category"]
        output_row['product__brand__name'] = input_row["brand"] 
        output_row['product__title'] = input_row["description"]
        output_row['product__description'] = input_row["long description"] 
        output_row['product__bullets__0'] = input_row["selling point 1"]
        output_row['product__bullets__1'] = input_row["selling point 2"]
        output_row['product__bullets__2'] = input_row["selling point 3"]
        output_row['product__bullets__3'] = input_row["selling point 4"]
        output_row['product__bullets__4'] = input_row["selling point 5"]
        output_row['product__bullets__5'] = input_row["selling point 6"]
        output_row['product__bullets__6'] = input_row["selling point 7"]
        output_row['product__configuration__codes'] = "" 
        output_row['product__multipack_quantity'] = ""
        output_row['product__country_of_origin__alpha_3'] = input_row["country of origin"]
        output_row['product__parent_sku'] = "" 
        output_row['attrib__arm_height'] = input_row["furniture arm height (inches)"]
        output_row['attrib__assembly_required'] = ""
        output_row['attrib__back_material'] = ""
        output_row['attrib__blade_finish'] = ""
        output_row['attrib__bulb_included'] = "True" if input_row["bulb 1 included"] == "Yes" else "False"
        output_row['attrib__bulb_type'] = input_row["bulb 1 type"]
        output_row['attrib__color'] = input_row["primary color family"]
        output_row['attrib__cord_length'] = input_row["cord length (inches)"]
        output_row['attrib__design_id'] = ""
        output_row['attrib__designer'] = ""
        output_row['attrib__distressed_finish'] = ""
        output_row['attrib__fill'] = ""
        output_row['attrib__finish'] = input_row["item finish"] 
        output_row['attrib__frame_color'] = ""
        output_row['attrib__hardwire'] = ""
        output_row['attrib__kit'] = input_row["conversion kit option"]
        output_row['attrib__leg_color'] = ""
        output_row['attrib__leg_finish'] = ""
        output_row['attrib__material'] = input_row["item materials"]
        output_row['attrib__number_bulbs'] = input_row["bulb 1 count"]
        output_row['attrib__orientation'] = ""
        output_row['attrib__outdoor_safe'] = ""
        output_row['attrib__pile_height'] = ""
        output_row['attrib__seat_depth'] = ""
        output_row['attrib__seat_height'] = input_row["furniture seat height (inches)"]
        output_row['attrib__seat_width'] = input_row["furniture seat dimensions (inches)"]
        output_row['attrib__shade'] = ""
        output_row['attrib__size'] = ""
        output_row['attrib__switch_type'] = input_row["switch type"]
        output_row['attrib__ul_certified'] = ""
        output_row['attrib__warranty_years'] = ""
        output_row['attrib__wattage'] = input_row["bulb 1 wattage"]
        output_row['attrib__weave'] = ""
        output_row['attrib__weight_capacity'] = input_row["furniture weight capacity (pounds)"]
        output_row['boxes__0__weight'] = input_row["carton 1 weight (pounds)"]
        output_row['boxes__0__length'] = input_row["carton 1 length (inches)"]
        output_row['boxes__0__height'] = input_row["carton 1 height (inches)"]
        output_row['boxes__0__width'] = input_row["carton 1 width (inches)"]
        output_row['boxes__1__weight'] = input_row["carton 2 weight (pounds)"] 
        output_row['boxes__1__length'] = input_row["carton 2 length (inches)"] 
        output_row['boxes__1__height'] = input_row["carton 2 height (inches)"] 
        output_row['boxes__1__width'] = input_row["carton 2 width (inches)"] 
        output_row['boxes__2__weight'] = input_row["carton 3 weight (pounds)"]  
        output_row['boxes__2__length'] = input_row["carton 3 length (inches)"] 
        output_row['boxes__2__height'] = input_row["carton 3 height (inches)"]  
        output_row['boxes__2__width'] = input_row["carton 3 width (inches)"]
        output_row['boxes__3__weight'] = ""
        output_row['boxes__3__length'] = ""
        output_row['boxes__3__height'] = ""
        output_row['boxes__3__width'] = ""
        output_row['product__styles'] = input_row["item style"]
        
        output_items.append(output_row)

    output_data = []
    for i, row in enumerate(output_items):
        output_data.append([])
        for header in output_header:
            output_data[i].append(output_items[i][header])
    
    return output_data



def main():
    output_header = ['manufacturer_sku', 'ean13', 'weight', 'length', 'width', 'height', 'prop_65', 'cost_price', 'min_price', 'made_to_order', 'product__product_class__name', 'product__brand__name', 'product__title', 'product__description', 'product__bullets__0', 'product__bullets__1', 'product__bullets__2', 'product__bullets__3', 'product__bullets__4', 'product__bullets__5', 'product__bullets__6', 'product__configuration__codes', 'product__multipack_quantity', 'product__country_of_origin__alpha_3', 'product__parent_sku', 'attrib__arm_height', 'attrib__assembly_required', 'attrib__back_material', 'attrib__blade_finish', 'attrib__bulb_included', 'attrib__bulb_type', 'attrib__color', 'attrib__cord_length', 'attrib__design_id', 'attrib__designer', 'attrib__distressed_finish', 'attrib__fill', 'attrib__finish', 'attrib__frame_color', 'attrib__hardwire', 'attrib__kit', 'attrib__leg_color', 'attrib__leg_finish', 'attrib__material', 'attrib__number_bulbs', 'attrib__orientation', 'attrib__outdoor_safe', 'attrib__pile_height', 'attrib__seat_depth', 'attrib__seat_height', 'attrib__seat_width', 'attrib__shade', 'attrib__size', 'attrib__switch_type', 'attrib__ul_certified', 'attrib__warranty_years', 'attrib__wattage', 'attrib__weave', 'attrib__weight_capacity', 'boxes__0__weight', 'boxes__0__length', 'boxes__0__height', 'boxes__0__width', 'boxes__1__weight', 'boxes__1__length', 'boxes__1__height', 'boxes__1__width', 'boxes__2__weight', 'boxes__2__length', 'boxes__2__height', 'boxes__2__width', 'boxes__3__weight', 'boxes__3__length', 'boxes__3__height', 'boxes__3__width', 'product__styles']

    with open("homework.csv", "r") as f:
        reader = csv.reader(f)
        input_header = next(reader)
        input_data = [row for row in reader]

    output_data = transform_data(input_header, input_data, output_header)

    with open("formatted.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(output_header)
        for row in output_data:
            writer.writerow(row)

if __name__ == "__main__":
    main()



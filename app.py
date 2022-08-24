# the purpose of this script is to read all of the rows of an unformatted .csv file and output them to a new file, formatted to specifications

import csv
import pycountry
import math

# specified output fields as per 'example.csv'
outputFields = ['manufacturer_sku','ean13','weight','length','width','height','prop_65','cost_price','min_price','made_to_order','product__product_class__name','product__brand__name','product__title','product__description','product__bullets__0','product__bullets__1','product__bullets__2','product__bullets__3','product__bullets__4','product__bullets__5','product__bullets__6','product__configuration__codes','product__multipack_quantity','product__country_of_origin__alpha_3','product__parent_sku','attrib__arm_height','attrib__assembly_required','attrib__back_material','attrib__blade_finish','attrib__bulb_included','attrib__bulb_type','attrib__color','attrib__cord_length','attrib__design_id','attrib__designer','attrib__distressed_finish','attrib__fill','attrib__finish','attrib__frame_color','attrib__hardwire','attrib__kit','attrib__leg_color','attrib__leg_finish','attrib__material','attrib__number_bulbs','attrib__orientation','attrib__outdoor_safe','attrib__pile_height','attrib__seat_depth','attrib__seat_height','attrib__seat_width','attrib__shade','attrib__size','attrib__switch_type','attrib__ul_certified','attrib__warranty_years','attrib__wattage','attrib__weave','attrib__weight_capacity','boxes__0__weight','boxes__0__length','boxes__0__height','boxes__0__width','boxes__1__weight','boxes__1__length','boxes__1__height','boxes__1__width','boxes__2__weight','boxes__2__length','boxes__2__height','boxes__2__width','boxes__3__weight','boxes__3__length','boxes__3__height','boxes__3__width','product__styles']

# this is used to bulk transform any output field in format 'attrib__'
def attrib_search(item, attrib):
    # remove 'attrib__'
    attrib = attrib[8:]
    # split attrib into search strings on '_'
    split_list = attrib.split('_')
    # search key list for a match to all substrings
    for key in item.keys():
        if all(x in key for x in split_list):
            return item[key]
    return ''

# this is used to bulk transform any output field in format 'boxes__'
def boxes_search(item, boxes):
    # remove 'boxes__'
    boxes = boxes[7:]
    # split on '__': will return a list in format ['int', 'attr' ]
    split_list = boxes.split('__')
    # add 1 to 'int' (box 0 in result correlates to carton 1 in raw data)
    # need to convert to int, then add 1, then back to to str
    split_list[0] = str(int(split_list[0]) + 1)
    # search key list for match to all substrings
    for key in item.keys():
        if all(x in key for x in split_list):
            match = item[key]
            if match == '':
                continue
            else:
                return str(math.ceil(float(item[key])))
    return ''

# open input file
with open('homework.csv', 'r') as file:
    reader = csv.DictReader(file)

    # open output file
    with open('formatted.csv', 'w') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(outputFields)

        for item in reader:
            # formatted data is stored in list 'f_item' of formatted item fields
            # at the end, each list of formatted values is written to output as a row
            f_item = []

            # field: manufacturer_sku (no formatting needed)
            f_item.append(item['item number'])

            # field: ean13
            f_upc = item['upc'] # need to add leading 0, and '-' at index 4 and -2
            if f_upc != '':
                f_upc = '0' + f_upc[:2] + '-' + f_upc[2:-1] + '-' + f_upc[-1]
            f_item.append(f_upc)

            # field: weight (round to 1st decimal)
            f_weight = item['item weight (pounds)']
            if f_weight != '':
                f_weight = round(float(f_weight), 1)
            f_item.append(f_weight)

            # field: length (round to 1st decimal)
            f_length = item['item depth (inches)']
            if f_length != '':
                f_length = round(float(f_length), 1)
            f_item.append(f_length)

            # field: width (round to 1st decimal)
            f_width = item['item width (inches)']
            if f_width != '':
                f_width = round(float(f_width), 1)
            f_item.append(f_width)
             
            # field: height (round to 1st decimal)
            f_height = item['item height (inches)']
            if f_height != '':
                f_height = round(float(f_height), 1)
            f_item.append(f_height)

            # field: prop_65 (check for url to california label)
            label_1 = item['url california label (jpg)']
            label_2 = item['url california label (pdf)']
            if label_1 != '' or label_2 != '':
                f_item.append('True')
            else:
                f_item.append('False')

            # field: cost_price
            # not sure how this data is supposed to be transformed
            # I'm guessing some calulation using inputs 'wholesale', 'map', 'msrp'
            # I'm assigning a placeholder value here with the assumption there is an internal calculation that was not specified for the scope of this assignment
            placeholder = '99.99'
            f_item.append(placeholder)


            # field: min_price
            # same as above field: not sure how to derive this value
            f_item.append(placeholder)

            # field: made_to_order
            # not sure how to derive this field, assuming it comes from the description
            desc = item['long description']
            if 'made to order' in desc:
                f_item.append('True')
            else:
                f_item.append('False')

            # field: product__product_class__name
            f_item.append(item['item category'])

            # field: product__brand__name
            f_item.append(item['brand'])

            # field: product__title
            f_title = item['description']
            f_item.append(f_title)

            # field: product__description
            # this could probably be condensed using string formatting
            f_desc = 'A ' + f_title.lower() + ' in a ' + item['item finish'].lower() + ' finish made of ' + item['item materials'].lower()
            f_item.append(f_desc)

            # field: product__bullets__0
            # not sure how this is derived
            f_item.append(item['selling point 1'])

            # field: product__bullets__1
            f_item.append(item['selling point 2'])

            # field: product__bullets__2
            f_item.append(item['selling point 3'])

            # field: product__bullets__3
            f_item.append(item['selling point 4'])

            # field: product__bullets__4
            f_item.append(item['selling point 5'])

            # field: product__bullets__5
            f_item.append(item['selling point 6'])

            # field: product__bullets__6
            f_item.append(item['selling point 7'])

            # field: product__configuration__codes
            f_pcc = ''
            if item['item finish'] != '':
                f_pcc = 'finish'
            f_item.append(f_pcc)

            # field: product__multipack_quantity
            f_item.append(item['carton count'])

            # field: product__country_of_origin__alpha_3
            long_country = item['country of origin']
            if long_country != '':
                try:
                    f_country = pycountry.countries.get(name=long_country).alpha_3
                except AttributeError:
                    continue
            f_item.append(f_country)
            
            # field: product__parent_sku
            # not sure how this is derived: assigned placeholder
            placeholder1 = 'A-9999999'
            f_item.append(placeholder1)

            # search for all 'attrib__' fields
            for i in range(25,59):
                f_item.append(attrib_search(item, outputFields[i]))

            # search for all 'boxes__' fields
            for i in range(59,75):
                f_item.append(boxes_search(item, outputFields[i]))
            
            # field: product__styles
            f_item.append(item['item style'])

            # end: write all formatted data to row
            writer.writerow(f_item)
import re
# creates new parent skus for items of the same type and formats them
parent_skus = {}
first_sku = 1000001
def get_parent_sku(item_type):
    global first_sku
    for name, sku in parent_skus.items():
        if name == item_type:
            return sku
    new_sku = "O-"+str(first_sku)
    first_sku += 1
    parent_skus[item_type] = new_sku
    return new_sku     

# Returns 3 digit country code
def get_country_code(country):
    if country == 'China':
        return 'CHN'
    elif country == 'Indonesia':
        return 'IDN'
    elif country == 'Vietnam':
        return 'VNM'
    elif country == 'India':
        return 'IND'
    else:
        return ''

new_lines = []
header = []
with open('homework.csv', encoding='utf8') as input:
    inp = input.read()
    # Splits input file into rows
    lines = inp.split('\n')
    # take header for final output
    header = lines[0].split(',')
    # remove header from list of rows
    del(lines[0])
    lines.pop()
    for l in lines:
        # removes commas that are not separating elements
        l = re.sub(r',\s', ' ', l)
        # splits the rows into columns
        line = l.split(',')
        # finds if item is prop 65 compliant
        def prop_65():
            if line[49] == '':
                return 'False'
            else:
                return 'True'
        # finds if item contains the word 'distressed' in its description
        def is_distressed():
            if 'distressed' in line[9].lower():
                return 'Yes'
            else:
                return ''
        # attributes schema for each line of the output file
        attributes = [
            line[0], line[1], line[19], line[16], line[15], line[17], prop_65(), line[6], line[7], 'False', line[12], line[11], line[9], line[10], line[135], line[136], line[137], line[138], line[139], line[140], line[141], '', line[4], get_country_code(line[129]), get_parent_sku(line[13]), line[125], '', '', '', line[83], line[81], line[89], line[114], '', '', is_distressed(), '', line[52], '', line[94], line[75], '', '', line[24], line[79], '', line[14], '', '', line[126], '', line[103], '', '', '', line[80], '', '', line[61], line[59], line[60], line[58], line[66], line[64], line[65], line[63], line[71], line[69], line[70], line[68], line[51]
        ]
        new_lines.append(attributes)
# Output code to formatted.csv file
with open('formatted.csv', 'a', encoding="utf-8") as output:
    # list of attributes for the header
    header_output = ['manufacturer_sku', 'ean13', 'weight', 'length', 'width', 'height', 'prop_65', 'cost_price', 'min_price', 'made_to_order', 'product__product_class__name', 'product__brand__name', 'product__title', 'product__description', 'product__bullets__0', 'product__bullets__1', 'product_bullets__2', 'product_bullets__3', 'product_bullets__4', 'product_bullets__5', 'product_bullets__6', 'product__configuration__codes', 'product__multipack__quantity', 'product__country_of_origin__alpha_3', 'product_parent_sku',  'attrib__arm_height', 'attrib__assembly_required', 'attrib__back_material', 'attrib__blade_finish', 'attrib__bulb_included', 'attrib__bulb_type', 'attrib__color', 'attrib__cord_length', 'attrib__design_id', 'attrib__designer', 'attrib__distressed_finish', 'attrib__fill', 'attrib_finish', 'attrib__frame_color', 'attrib__hardwire', 'attrib_kit', 'attrib__leg_color', 'attrib__leg_finish', 'attrib__material', 'attrib__number_bulbs', 'attrib__orientation', 'attrib__outdoor_safe', 'attrib__pile_height', 'attrib__seat_depth', 'attrib__seat_height', 'attrib__seat_width', 'attrib__shade', 'attrib_size', 'attrib__switch_type', 'attrib__ul_certified', 'attrib__warranty_years', 'attrib_wattage', 'attrib__weave', 'attrib__weight_capacity', 'boxes__0__weight', 'boxes__0__length', 'boxes__0__height', 'boxes__0__width', 'boxes__1__weight', 'boxes__1__length', 'boxes__1__height', 'boxes__1__width', 'boxes__2__weight', 'boxes__2__length', 'boxes__2__height', 'boxes__2__width', 'boxes__3__weight', 'boxes__3__length', 'boxes__3__height', 'boxes__3__width', 'product__styles']
    # add back header to final output
    for item in header_output:
        output.write(item)
        output.write(',')
    output.write('\n')
    # final output of rearranged lines
    for line in new_lines:
        line_output = [str(item) + "," for item in line[:-1]]
        for item in line_output:
            output.write(item)
        output.write('\n')

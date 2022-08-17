import pandas

def format_upc(number):
  '''
  This function formats the upc number from the original data set to the ean13 number requried by the example documentation in the final dataset.
  '''
  number = str(number)
  if len(number) >= 11:
    formatted = "0" + number[:2] + "-" + number[2:11] + "-" + number[11]
    return formatted

def prop_65_format(string):
  '''
  This function acknowledges if there is a picture for prop_65 and if there is it changes that string to a boolean of True or False based on the existance of the picture(url).
  '''
  if string != "":
    return True
  else:
    return False

'''
Grabs needed columns from homework.csv and creates a new data set with those colums.
'''
df = pandas.read_csv('homework.csv', usecols=['item number', 'upc', 'item weight (pounds)', 'item depth (inches)', 'item width (inches)', 'item height (inches)', 'url california label (jpg)', 'item category', 'brand', 'description', 'long description', 'carton count', 'country of origin', 'furniture arm height (inches)', 'bulb 1 included', 'bulb 1 type', 'primary color family', 'cord length (inches)', 'item finish', 'conversion kit option', 'item materials', 'bulb 1 count', 'outdoor', 'furniture seat height (inches)', 'furniture seat dimensions (inches)', 'shade/glass description', 'switch type', 'safety rating', 'bulb 1 wattage', 'furniture weight capacity (pounds)', 'carton 1 weight (pounds)', 'carton 1 length (inches)', 'carton 1 height (inches)', 'carton 1 width (inches)', 'carton 2 weight (pounds)', 'carton 2 length (inches)', 'carton 2 height (inches)', 'carton 2 width (inches)', 'carton 3 weight (pounds)', 'carton 3 length (inches)', 'carton 3 height (inches)', 'carton 3 width (inches)', 'item style'])

'''
formats the upc and url califonia label columns with the specified functions.
'''
df['upc'] = df['upc'].apply(format_upc)
df['url california label (jpg)'] = df['url california label (jpg)'].apply([prop_65_format])

'''
Renames the colmns as needed. 
'''
df.rename(columns={
  'item number': 'manufacturer_sku',
  'upc': 'ean13',
  'item weight (pounds)': 'weight',
  'item depth (inches)': 'length',
  'item width (inches)': 'width',
  'item height (inches)': 'height',
  'url california label (jpg)': 'prop_65',
  'item category': 'product__product_class__name',
  'brand': 'product__brand__name',
  'description': 'product__title',
  'long description': 'product__description',
  'carton count': 'product__multipack_quantity',
  'country of origin': 'product__country_of_origin__alpha_3',
  'furniture arm height (inches)': 'attrib__arm_height',
  'bulb 1 included': 'attrib__bulb_included',
  'bulb 1 type': 'attrib__bulb_type',
  'primary color family': 'attrib__color',
  'cord length (inches)': 'attrib__cord_length',
  'item finish': 'attrib__finish',
  'conversion kit option': 'attrib__kit',
  'item materials': 'attrib__material',
  'bulb 1 count': 'attrib__number_bulbs',
  'outdoor': 'attrib__outdoor_safe',
  'furniture seat height (inches)': 'attrib__seat_height',
  'furniture seat dimensions (inches)': 'attrib__seat_width',
  'shade/glass description': 'attrib__shade',
  'switch type': 'attrib__switch_type',
  'safety rating': 'attrib__ul_certified',
  'bulb 1 wattage': 'attrib__wattage',
  'furniture weight capacity (pounds)': 'attrib__weight_capacity',
  'carton 1 weight (pounds)': 'boxes__0__weight',
  'carton 1 length (inches)': 'boxes__0__length',
  'carton 1 height (inches)': 'boxes__0__height',
  'carton 1 width (inches)': 'boxes__0__width',
  'carton 2 weight (pounds)': 'boxes__1__weight',
  'carton 2 length (inches)': 'boxes__1__length',
  'carton 2 height (inches)': 'boxes__1__height',
  'carton 2 width (inches)': 'boxes__1__width',
  'carton 3 weight (pounds)': 'boxes__2__weight',
  'carton 3 length (inches)': 'boxes__2__length',
  'carton 3 height (inches)': 'boxes__2__height',
  'carton 3 width (inches)': 'boxes__2__width',
  'item style': 'product__styles',
  }, inplace=True)

'''
Writes the dataframe to a new csv file. 
'''
df.to_csv('formatted.csv')

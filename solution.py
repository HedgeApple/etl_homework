import csv
import pandas as pd
import re

if __name__=='__main__':
#Retriving the Headers from the example.csv file
    with open('example.csv', 'r', encoding="utf-8") as f:
        f_reader = csv.reader(f)
        header =[]
        header = next(f_reader)
        
    #Renaming the headers from homework.csv using pandas and saving it to new homework1.csv to retain original homework.csv file
    df = pd.read_csv("homework.csv", encoding="utf-8")

    df.rename(columns={"item weight (pounds)": "weight",
                       'item depth (inches)':'length',
                       'item height (inches)':'height',
                       'item width (inches)':'width', 
                       'wholesale ($)':'cost_price',
                       'map ($)':'min_price',
                       'description':'product_title',
                       'long description':'product_description',
                       'brand':'product__brand__name',
                       'item category':'product__product_class__name',
                       'item materials':'attrib__material',
                       'item finish':'attrib__finish',
                       'bulb 1 count':'attrib__number_bulbs',
                       'bulb 1 type':'attrib__bulb_type',
                       'switch type':'attrib__switch_type',
                       'bulb 1 wattage':'attrib__wattage',
                       'outdoor':'attrib__outdoor_safe',
                       'primary color family':'attrib__color',
                       'carton 1 width (inches)':'boxes__0__width',
                       'carton 1 length (inches)':'boxes__0__length',
                       'carton 1 height (inches)':'boxes__0__height',
                       'carton 1 weight (pounds)':'boxes__0__weight',
                       'carton 2 width (inches)':'boxes__1__width',
                       'carton 2 length (inches)':'boxes__1__length',
                       'carton 2 height (inches)':'boxes__1__height',
                       'carton 2 weight (pounds)':'boxes__1__weight',
                       'carton 3 width (inches)':'boxes__2__width',
                       'carton 3 length (inches)':'boxes__2__length',
                       'carton 3 height (inches)':'boxes__2__height',
                       'carton 3 weight (pounds)':'boxes__2__weight',
                       'conversion kit option':'attrib__kit',
                       'safety rating':'attrib__ul_certified', #convert UL to YES else to NO
                       'cord length (inches)':'attrib__cord_length',
                       'furniture arm height (inches)': 'attrib__arm_height',
                       'furniture seat height (inches)':'attrib__seat_height',
                       'furniture seat dimensions (inches)':'attrib__seat_width', #change
                       'furniture weight capacity (pounds)':'attrib__weight_capacity',
                       'country of origin':'product__country_of_origin__alpha_3',
                       'product_title' : 'product__title',
                       'long description' : 'product__description',
                      'item style':'product__styles',}, inplace=True)

    df.to_csv('homework1.csv', index=False)
    
    #creating a list with the updated Headers from homework(1).csv
    with open('homework1.csv', 'r', encoding="utf-8") as e:
        e_reader = csv.reader(e)
        header2 =[]
        header2 = next(e_reader)
        
    #creating a list with Headers that were common to both example.csv and UPDATED homework(1).csv
    common = list(set(header).intersection(header2))

    #creating new csv file and removing datasets not present/required according to example.csv, saving to new homework2.csv
    df2 = pd.read_csv("homework1.csv", encoding="utf-8")
    keep_col = common
    dfChanged = df2[keep_col]
    dfChanged.to_csv('homework2.csv', index=False)
    
#filling up the rows of homework(3).csv with data
    with open('homework2.csv', 'r', encoding="utf-8") as g:
        g_reader = csv.DictReader(g)
        #next(g_reader)
        with open('homework3.csv', 'w', encoding="utf-8") as h:
            csv_writer = csv.DictWriter(h, header, lineterminator ='\n')
            csv_writer.writeheader()
            csv_writer.writerows(g_reader)
            
   #making final adjustments to some values in attrib__ul_certified, product__country_of_origin__alpha_3 and attrib__seat_width columns
    dframe = pd.read_csv("homework3.csv")
    a = len(dframe)

    #changing from float to string to add 'Yes/NO' values
    dframe['attrib__distressed_finish'] = dframe['attrib__distressed_finish'].map(str)

    for numb in range(0,a):

        #Changing UL certified from 'UL' to either 'YES' or 'NO'
        if dframe.at[numb,'attrib__ul_certified'] == 'UL': 
            dframe.at[numb,'attrib__ul_certified'] = 'YES'
        else:
            dframe.at[numb,'attrib__ul_certified'] = 'NO'    

        #Changing name of Countries to 3 digit ALPHA
        word = (dframe.at[numb,'product__country_of_origin__alpha_3'])
        if type(word) == str:
            (dframe.at[numb,'product__country_of_origin__alpha_3']) = word[0:3].upper()

        seat_width = (dframe.at[numb,'attrib__seat_width'])
        if type(seat_width) == str:
            dframe.at[numb,'attrib__seat_width']= seat_width.split('x')[0]

        #removing '$' signs and ',' from prices to round off to 2 decimal
        cost = str(dframe.at[numb,'cost_price'])
        cost = re.sub('[$,]', '', cost)
        cost = float(cost)
        dframe.at[numb,'cost_price'] = round(cost, 2)

        mini = str(dframe.at[numb,'min_price'])
        mini = re.sub('[$,]', '', mini)
        mini = float(mini)
        dframe.at[numb,'cost_price'] = round(mini, 2)

        #adding Yes/No values to attrib__distressed_finish
        fullstring = str(dframe.at[numb,'product__description'])
        substring = "[Dd]istress"

        if re.search(substring, fullstring):
            dframe.at[numb,'attrib__distressed_finish'] = 'Yes' 
        else:
            dframe.at[numb,'attrib__distressed_finish'] = 'No'

    dframe.to_csv('formatted.csv', index=False) 

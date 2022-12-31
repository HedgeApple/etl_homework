"""
    31/12/2022
    Author: Oussama Mechri
    Description: Solution for etl homework job application for hedgeapple
"""
import pandas as pd
import datetime
import pycountry


# load all colors names from online dataset for colors extraction when needed
colorsCSV = pd.read_csv(
    "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv",
    header=None)

# hardcode filling types and weaves to later
# extract from description when needed
fillings = ["hollowfibre", "microfibre", "feather",
            "down", "foam", "latex", "bead", "water", "buckwheat"]

weaves = ["handtufted", "handknotted", "flatweave", "braided"]

# load homework as originalCSV to extract data from.
originalCSV = pd.read_csv("./homework.csv",
                          dtype={
                              "upc": str,
                              "wholesale ($)": str,
                              "map ($)": str,
                              "multi-piece dimension 4 (inches)": str,
                              "url drawing": str,
                              "url animated gif": str,
                              "bulb 2 type": str,
                              "bulb 2 base": str,
                              "color temperature": str,
                              "cri": str,
                              "drawer 1 interior dimensions (inches)": str,
                              "drawer 2 interior dimensions (inches)": str,
                              "drawer 3 interior dimensions (inches)": str
                          })


# date was not needed in example.csv but this is an approach as requested
def formatDate(date: str):
    rawDate = datetime.datetime.strptime(date, "%m/%d/%Y")
    return rawDate.strftime("%Y-%m-%d")


# convert Yes/No data to True False as in example.csv
def toBool(text):
    text = str(text)
    if text.lower() == "yes":
        return True
    elif text.lower() == "no":
        return False
    else:
        return ""


# convert UPC to EAN
def upcEan13(upc):
    ean = "0" + str(upc)
    return ean[:2] + "-" + ean[2:12] + "-" + ean[-1]


# remove $ sign if present in values
def formatCurrency(data):
    return round(float(str(data).replace("$", "").replace(",", "")), 2)


# not needed column but a way to convert qubic foot to qubic inch 
def convertFeetInches(val: float):
    return val * 1728


# extract alpha3 countries from pycountry data
def alpha3Country(country):
    if not isinstance(country, str):
        return ""
    specialCases = {
        "Vietnam": "Viet Nam",
        "Phillipines": "Philippines",
    }
    if country in specialCases:
        country = specialCases[country]
    for count in pycountry.countries:
        if country.lower() in count.name.lower():
            return count.alpha_3


#check presense of image and document for prop65
def prop65(img, doc):
    if pd.isna(img) or pd.isna(doc):
        return False
    else:
        return True


def getSeatDepth(dimensions):
    try:
        return dimensions.split("x")[0]
    except BaseException:
        return ""


def getSeatWidth(dimensions):
    try:
        return dimensions.split("x")[1]
    except BaseException:
        return ""


def checkShade(text: str):
    if "No Shade" in text:
        return "No"
    else:
        return "Yes"


def checkDistressed(data):
    if "distressed" in str(data).lower():
        return True
    else:
        return False


def sizeClass(text):
    data = text.lower().split("-")
    if "large" in data[-1]:
        return "Large"
    elif "medium" in data[-1]:
        return "Medium"
    elif "small" in data[-1]:
        return "Small"
    else:
        return ""


def checkUL(data):
    if "ul" in str(data).lower():
        return True
    else:
        return False


def checkWeave(_type, description):
    if "Rug" in _type:
        if any((found := item) in description.lower() for item in weaves):
            return found


def checkOrder(qty):
    if int(qty) < 1:
        return False
    else:
        return True


def assemblyRequired(data):
    if "assembl" in str(data):
        return True
    else:
        return ""


def checkFill(_type, description):
    if "Pillow" or "Pouf" in _type and "fill" in description.lower():
        if any((found := item) in description.lower() for item in fillings):
            return found


def findColors(description, _type):
    if "Picture Frame" in _type:
        if any((found := item) in description.lower()
               for item in colorsCSV[1].str.lower()):
            return found


def checkWire(switch):
    if not isinstance(switch, str):
        return False
    if "Hardwired" in str(switch):
        return True
    else:
        return False


# create final dataframe to respect data types and requested formats
formattedCSV = pd.DataFrame({
    "manufacturer_sku": originalCSV['item number'],
    "ean13": originalCSV['upc'].apply(upcEan13),
    "weight": originalCSV['item weight (pounds)'],
    "length": originalCSV['item depth (inches)'],
    "width": originalCSV['item width (inches)'],
    "height": originalCSV['item height (inches)'],
    "prop_65": originalCSV.apply(lambda x: prop65(
        x['url california label (jpg)'],
        x['url california label (pdf)']), axis=1),
    "cost_price": originalCSV['wholesale ($)'].apply(formatCurrency),
    "min_price": originalCSV['map ($)'].apply(formatCurrency),
    "made_to_order": originalCSV['min order qty'].apply(checkOrder),
    "product__product_class__name": originalCSV['item category'],
    "product__brand__name": originalCSV['brand'],
    "product__title": originalCSV['description'],
    "product__description": originalCSV['long description'],
    "product__bullets__0": originalCSV['selling point 1'],
    "product__bullets__1": originalCSV['selling point 2'],
    "product__bullets__2": originalCSV['selling point 3'],
    "product__bullets__3": originalCSV['selling point 4'],
    "product__bullets__4": originalCSV['selling point 5'],
    "product__bullets__5": originalCSV['selling point 6'],
    "product__bullets__6": originalCSV['selling point 7'],
    "product__configuration__codes": None,
    "product__multipack_quantity": pd.Series(
        originalCSV['carton count'],
        dtype='object'),
    "product__country_of_origin__alpha_3": originalCSV['country of origin'].apply(alpha3Country),
    "product__parent_sku": None,
    "attrib__arm_height": originalCSV['furniture arm height (inches)'],
    "attrib__assembly_required": originalCSV['selling point 2'].apply(assemblyRequired),
    "attrib__back_material": None,
    "attrib__bulb_included": originalCSV['bulb 1 included'].apply(toBool),
    "attrib__bulb_type": originalCSV['bulb 1 type'],
    "attrib__color": originalCSV['primary color family'],
    "attrib__cord_length": originalCSV['cord length (inches)'],
    "attrib__design_id": None,
    "attrib__designer": originalCSV['licensed by'],
    "attrib__distressed_finish": originalCSV['item finish'].apply(checkDistressed),
    "attrib__fill": originalCSV.apply(lambda x: checkFill(
        x['item type'],
        x['description']), axis=1),
    "attrib__finish": originalCSV['item finish'],
    "attrib__frame_color": originalCSV.apply(lambda x: findColors(
        x['description'],
        x['item type']), axis=1),
    "attrib__hardwire": originalCSV['switch type'].apply(checkWire),
    "attrib__kit": originalCSV['conversion kit option'].apply(toBool),
    "attrib__leg_color": None,
    "attrib__leg_finish": None,
    "attrib__material": originalCSV['item materials'],
    "attrib__number_bulbs": originalCSV['bulb 1 count'],
    "attrib__orientation": None,
    "attrib__outdoor_safe": originalCSV['outdoor'].apply(toBool),
    "attrib__pile_height": originalCSV['max overall height (inches)'],
    "attrib__seat_depth": originalCSV['furniture seat dimensions (inches)'].apply(getSeatDepth),
    "attrib__seat_height": originalCSV['furniture seat height (inches)'],
    "attrib__seat_width": originalCSV['furniture seat dimensions (inches)'].apply(getSeatWidth),
    "attrib__shade": originalCSV['shade/glass description'],
    "attrib__size": originalCSV['description'].apply(sizeClass),
    "attrib__switch_type": originalCSV['switch type'],
    "attrib__ul_certified": originalCSV['safety rating'].apply(checkUL),
    "attrib__warranty_years": None,
    "attrib__wattage": originalCSV['bulb 1 wattage'],
    "attrib__weave": originalCSV.apply(lambda x: checkWeave(
        x['item type'],
        x['description']), axis=1),
    "attrib__weight_capacity": originalCSV['furniture weight capacity (pounds)'],
    "boxes__0__weight": originalCSV['carton 1 weight (pounds)'],
    "boxes__0__length": originalCSV['carton 1 length (inches)'],
    "boxes__0__height": originalCSV['carton 1 height (inches)'],
    "boxes__0__width": originalCSV['carton 1 width (inches)'],
    "boxes__1__weight": originalCSV['carton 2 weight (pounds)'],
    "boxes__1__length": originalCSV['carton 2 length (inches)'],
    "boxes__1__height": originalCSV['carton 2 height (inches)'],
    "boxes__1__width": originalCSV['carton 2 width (inches)'],
    "boxes__2__weight": originalCSV['carton 3 weight (pounds)'],
    "boxes__2__length": originalCSV['carton 3 length (inches)'],
    "boxes__2__height": originalCSV['carton 3 height (inches)'],
    "boxes__2__width": originalCSV['carton 3 width (inches)'],
    "product__styles": originalCSV['item style']
})


formattedCSV = formattedCSV.convert_dtypes()
formattedCSV.to_csv("./formatted.csv")

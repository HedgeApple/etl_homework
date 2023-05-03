import pandas as pd
import pycountry


class Converter():
    def __init__(self) -> None:
        self.df = pd.read_csv("homework.csv", low_memory=False)

    # this function will convert dates to iso 8601 format. Example.csv did not include date,
    # so I did not call this during the export
    def convertDate(date):
        return pd.to_datetime(date, format="%m/%d/%y").dt.strftime('%Y-%m-%d')

    # fills the prop65 bool value of a product
    def prop65(self, jpg, pdf):
        return False if (pd.isna(jpg) or pd.isna(pdf)) else True

    # converts currency into float, and parses out symbols if needed
    def convert_curreny_type(self, unit):
        return float(str(unit).replace("$", "").replace(",", ""))

    # convets cubic feet to cubic inches
    def dimension_to_inches(self,  dim):
        return dim * (12**3)

    # converts upc codes into ean13 codes per the example file
    def upc_to_ean13(self, upc):
        ean13 = str(upc)
        return "0" + ean13[:2] + "-" + ean13[2:11] + "-" + ean13[-1]

    # converts country name to alpha3 format
    def alpha3(self, country):
        if not isinstance(country, str):
            return ""
        if not pycountry.countries.get(name=country):
            return ""
        else:
            return pycountry.countries.get(name=country).alpha_3

    # gets the size of an item based on if it is in the description
    def getSize(self, desc):
        lower = desc.lower()
        if "sm" in lower or "small" in lower:
            return "Small"
        elif "md" in lower or "medium" in lower:
            return "Medium"
        elif "lg" in lower or "large" in lower:
            return "Large"
        else:
            return ""

    # exports the formatted.csv file with all of the needed headers based off example.csv
    def export(self):

        # fix spelling mistakes of two countries
        self.df["country of origin"] = self.df["country of origin"].replace(
            ["Phillipines", "Vietnam"], ["Philippines", "Viet Nam"]
        )

        formattedcsv = pd.DataFrame({
            "manufacturer_sku": self.df['item number'],
            "ean13": self.df['upc'].apply(self.upc_to_ean13),
            "weight": self.df['item weight (pounds)'],
            "length": self.df['item depth (inches)'],
            "width": self.df['item width (inches)'],
            "height": self.df['item height (inches)'],
            "prop_65": self.df.apply(lambda x: self.prop65(
                x['url california label (jpg)'],
                x['url california label (pdf)']), axis=1),
            "cost_price": self.df['wholesale ($)'].apply(self.convert_curreny_type),
            "min_price": self.df['map ($)'].apply(self.convert_curreny_type),
            "made_to_order": self.df['min order qty'].apply(lambda x: True if int(x) >= 1 else False),
            "product__product_class__name": self.df['item category'],
            "product__brand__name": self.df['brand'],
            "product__title": self.df['description'],
            "product__description": self.df['long description'],
            "product__bullets__0": self.df['selling point 1'],
            "product__bullets__1": self.df['selling point 2'],
            "product__bullets__2": self.df['selling point 3'],
            "product__bullets__3": self.df['selling point 4'],
            "product__bullets__4": self.df['selling point 5'],
            "product__bullets__5": self.df['selling point 6'],
            "product__bullets__6": self.df['selling point 7'],
            "product__configuration__codes": None,
            "product__multipack_quantity": pd.Series(self.df['carton count'], dtype='object'),
            "product__country_of_origin__alpha_3": self.df['country of origin'].apply(self.alpha3),
            "product__parent_sku": None,
            "attrib__arm_height": self.df['furniture arm height (inches)'],
            "attrib__assembly_required": self.df['selling point 2'].apply(lambda x: True if "assemble" in str(x) else False),
            "attrib__back_material": None,
            "attrib__bulb_included": self.df['bulb 1 included'].apply(lambda x: True if str(x).lower() == "yes" else False),
            "attrib__leg_color": None,
            "attrib__leg_finish": None,
            "attrib__material": self.df['item materials'],
            "attrib__number_bulbs": self.df['bulb 1 count'],
            "attrib__orientation": None,
            "attrib__outdoor_safe": self.df['outdoor'].apply(lambda x: True if str(x).lower() == "yes" else False),
            "attrib__pile_height": self.df['max overall height (inches)'],
            "attrib__seat_depth": self.df['furniture seat dimensions (inches)'],
            "attrib__seat_height": self.df['furniture seat height (inches)'],
            "attrib__seat_width": self.df['furniture seat dimensions (inches)'],
            "attrib__shade": self.df['shade/glass description'],
            "attrib__size": self.df['description'].apply(self.getSize),
            "attrib__switch_type": self.df['switch type'],
            "attrib__ul_certified": self.df['safety rating'].apply(lambda x: True if "ul" in str(x).lower() else False),
            "attrib__warranty_years": None,
            "attrib__wattage": self.df['bulb 1 wattage'],
            "attrib__weight_capacity": self.df['furniture weight capacity (pounds)'],
            "boxes__0__weight": self.df['carton 1 weight (pounds)'],
            "boxes__0__length": self.df['carton 1 length (inches)'],
            "boxes__0__height": self.df['carton 1 height (inches)'],
            "boxes__0__width": self.df['carton 1 width (inches)'],
            "boxes__1__weight": self.df['carton 2 weight (pounds)'],
            "boxes__1__length": self.df['carton 2 length (inches)'],
            "boxes__1__height": self.df['carton 2 height (inches)'],
            "boxes__1__width": self.df['carton 2 width (inches)'],
            "boxes__2__weight": self.df['carton 3 weight (pounds)'],
            "boxes__2__length": self.df['carton 3 length (inches)'],
            "boxes__2__height": self.df['carton 3 height (inches)'],
            "boxes__2__width": self.df['carton 3 width (inches)'],
            "product__styles": self.df['item style']
        })

        formattedcsv = formattedcsv.to_csv("./formatted.csv")


if __name__ == "__main__":
    Converter().export()

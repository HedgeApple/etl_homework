import pandas as pd
import pycountry
import time
import re

start_time = time.time()

with open("homework.csv", encoding="UTF-8") as input_file:
    data = pd.read_csv(input_file, sep=",", dtype="object")

    # Rename columns which will appear in formatted.csv more or less as they are
    data.rename(
        columns={
            "item number": "manufacturer_sku",
            "item weight (pounds)": "weight",
            "item depth (inches)": "length",
            "item width (inches)": "width",
            "item height (inches)": "height",
            "wholesale ($)": "cost_price",
            "map ($)": "min_price",
            "item category": "product__product_class__name",
            "brand": "product__brand__name",
            "description": "product__title",
            "long description": "product__description",
            "selling point 1": "product__bullets__0",
            "selling point 2": "product__bullets__1",
            "selling point 3": "product__bullets__2",
            "selling point 4": "product__bullets__3",
            "selling point 5": "product__bullets__4",
            "selling point 6": "product__bullets__5",
            "selling point 7": "product__bullets__6",
            "carton count": "product__multipack_quantity",
            "country of origin": "product__country_of_origin__alpha_3",
            "furniture arm height (inches)": "attrib__arm_height",
            "bulb 1 included": "attrib__bulb_included",
            "bulb 1 type": "attrib__bulb_type",
            "primary color family": "attrib__color",
            "cord length (inches)": "attrib__cord_length",
            "licensed by": "attrib__designer",
            "item finish": "attrib__finish",
            "conversion kit option": "attrib__kit",
            "item materials": "attrib__material",
            "bulb 1 count": "attrib__number_bulbs",
            "outdoor": "attrib__outdoor_safe",
            "furniture seat height (inches)": "attrib__seat_height",
            "shade/glass description": "attrib__shade",
            "switch type": "attrib__switch_type",
            "bulb 1 wattage": "attrib__wattage",
            "furniture weight capacity (pounds)": "attrib__weight_capacity",
            "carton 1 weight (pounds)": "boxes__0__weight",
            "carton 1 length (inches)": "boxes__0__length",
            "carton 1 height (inches)": "boxes__0__height",
            "carton 1 width (inches)": "boxes__0__width",
            "carton 2 weight (pounds)": "boxes__1__weight",
            "carton 2 length (inches)": "boxes__1__length",
            "carton 2 height (inches)": "boxes__1__height",
            "carton 2 width (inches)": "boxes__1__width",
            "carton 3 weight (pounds)": "boxes__2__weight",
            "carton 3 length (inches)": "boxes__2__length",
            "carton 3 height (inches)": "boxes__2__height",
            "carton 3 width (inches)": "boxes__2__width",
            "item style": "product_styles",
        },
        inplace=True,
    )

    def convert_upc_ean13(upc):
        try:
            upc = str(int(upc))
        except ValueError:
            # print("Invalid UPC: ", upc)
            return None
        upc = "0" * (12 - len(upc)) + upc
        ean13 = "0" + upc[:2] + "-" + upc[2:11] + "-" + upc[11]
        return ean13

    def convert_country_alpha3(country_name):
        spelling_changes = {"Vietnam": "Viet Nam", "Phillipines": "Philippines"}
        if country_name in spelling_changes:
            country_name = spelling_changes[country_name]
        try:
            return pycountry.countries.get(name=country_name).alpha_3
        except LookupError:
            return None
        except AttributeError:
            # print("Country name not recognized: ", country_name)
            return None

    def check_prop_65(url_jpg, url_pdf):
        if not url_jpg.empty or not url_pdf.empty:
            return True
        else:
            return False

    def check_attribute(data_cell, attribute):
        if str(attribute).lower() in str(data_cell).lower():
            return True
        else:
            return False

    def parse_dimension(dimensions, height, index):
        if type(dimensions) == float:
            return dimensions
        else:
            dimensions_array = re.split("x|X|\*", dimensions, maxsplit=2)
            if len(dimensions_array) == 3:
                height = float(height)
                dimensions_array = list(map(lambda x: float(x), dimensions_array))
                length_width = list(filter(lambda x: x != height, dimensions_array))
                return float(length_width[index])
            elif len(dimensions_array) == 2:
                return float(dimensions_array[index])
            else:
                return float(dimensions_array[0])

    def format_currency(data_cell, currency_sign):
        try:
            return float(data_cell)
        except ValueError:
            data_cell = data_cell.replace(currency_sign, "")
            data_cell = data_cell.replace(",", "")
            return round(float(data_cell), 2)

    # Do formatting for columns that require it

    data["ean13"] = data["upc"].apply(convert_upc_ean13)
    data["cost_price"] = data["cost_price"].apply(format_currency, currency_sign="$")
    data["min_price"] = data["min_price"].apply(format_currency, currency_sign="$")

    data["prop_65"] = check_prop_65(
        data["url california label (jpg)"], data["url california label (pdf)"]
    )

    data["product__country_of_origin__alpha_3"] = data[
        "product__country_of_origin__alpha_3"
    ].apply(convert_country_alpha3)

    data["attrib__distressed_finish"] = data["attrib__finish"].apply(
        check_attribute, attribute="distressed"
    )

    data["attrib__seat_depth"] = data.apply(
        lambda x: parse_dimension(
            dimensions=x["furniture seat dimensions (inches)"],
            height=x["attrib__seat_height"],
            index=0,
        ),
        axis=1,
    )

    data["attrib__seat_width"] = data.apply(
        lambda x: parse_dimension(
            dimensions=x["furniture seat dimensions (inches)"],
            height=x["attrib__seat_height"],
            index=1,
        ),
        axis=1,
    )

    data["attrib__ul_certified"] = data["safety rating"].apply(
        check_attribute, attribute="ul"
    )

    # Initialize unknown columns to None (unsure of where this information is sourced from)

    data["made_to_order"] = None
    data["product__configuration__codes"] = None
    data["product__parent_sku"] = None
    data["attrib__assembly_required"] = None
    data["attrib__back_material"] = None
    data["attrib__blade_finish"] = None
    data["attrib__design_id"] = None
    data["attrib__fill"] = None
    data["attrib__frame_color"] = None
    data["attrib__hardwire"] = None
    data["attrib__leg_color"] = None
    data["attrib__leg_finish"] = None
    data["attrib__orientation"] = None
    data["attrib__pile_height"] = None
    data["attrib__size"] = None
    data["attrib__warranty_years"] = None
    data["attrib__weave"] = None
    data["boxes__3__weight"] = None
    data["boxes__3__length"] = None
    data["boxes__3__height"] = None
    data["boxes__3__width"] = None

    data = data.astype(
        {
            "weight": "float64",
            "length": "float64",
            "width": "float64",
            "height": "float64",
            "made_to_order": "bool",
            "attrib__warranty_years": "float64",
            "attrib__cord_length": "float64",
            "attrib__arm_height": "float64",
            "attrib__weight_capacity": "float64",
            "attrib__pile_height": "float64",
            "attrib__number_bulbs": "float64",
            "boxes__0__weight": "float64",
            "boxes__0__length": "float64",
            "boxes__0__height": "float64",
            "boxes__0__width": "float64",
            "boxes__1__weight": "float64",
            "boxes__1__length": "float64",
            "boxes__1__height": "float64",
            "boxes__1__width": "float64",
            "boxes__2__weight": "float64",
            "boxes__2__length": "float64",
            "boxes__2__height": "float64",
            "boxes__2__width": "float64",
            "boxes__3__weight": "float64",
            "boxes__3__length": "float64",
            "boxes__3__height": "float64",
            "boxes__3__width": "float64",
        }
    )

    data = data[
        [
            "manufacturer_sku",
            "ean13",
            "weight",
            "length",
            "width",
            "height",
            "prop_65",
            "cost_price",
            "min_price",
            "made_to_order",
            "product__product_class__name",
            "product__brand__name",
            "product__title",
            "product__description",
            "product__bullets__0",
            "product__bullets__1",
            "product__bullets__2",
            "product__bullets__3",
            "product__bullets__4",
            "product__bullets__5",
            "product__bullets__6",
            "product__configuration__codes",
            "product__multipack_quantity",
            "product__country_of_origin__alpha_3",
            "product__parent_sku",
            "attrib__arm_height",
            "attrib__assembly_required",
            "attrib__back_material",
            "attrib__blade_finish",
            "attrib__bulb_included",
            "attrib__bulb_type",
            "attrib__color",
            "attrib__cord_length",
            "attrib__design_id",
            "attrib__designer",
            "attrib__distressed_finish",
            "attrib__fill",
            "attrib__finish",
            "attrib__frame_color",
            "attrib__hardwire",
            "attrib__kit",
            "attrib__leg_color",
            "attrib__leg_finish",
            "attrib__material",
            "attrib__number_bulbs",
            "attrib__orientation",
            "attrib__outdoor_safe",
            "attrib__pile_height",
            "attrib__seat_depth",
            "attrib__seat_height",
            "attrib__seat_width",
            "attrib__shade",
            "attrib__size",
            "attrib__switch_type",
            "attrib__ul_certified",
            "attrib__warranty_years",
            "attrib__wattage",
            "attrib__weave",
            "attrib__weight_capacity",
            "boxes__0__weight",
            "boxes__0__length",
            "boxes__0__height",
            "boxes__0__width",
            "boxes__1__weight",
            "boxes__1__length",
            "boxes__1__height",
            "boxes__1__width",
            "boxes__2__weight",
            "boxes__2__length",
            "boxes__2__height",
            "boxes__2__width",
            "boxes__3__weight",
            "boxes__3__length",
            "boxes__3__height",
            "boxes__3__width",
            "product_styles",
        ]
    ]

    pd.set_option("display.max_rows", None)
    # print(data.dtypes)

    data = data.fillna("")
    data.to_csv("formatted.csv", index=False)

    # print(data)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)

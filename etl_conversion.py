#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  etl_conversion.py
#
#  Copyright 2022 Stephan Schonberg <solecism@gmail.com>

import csv
from iso3166 import countries


def currency(amount):
    # guidelines indicate rounding to the nearest cent
    # formatting example shows no dollar sign
    # no guidance on commas, I choose to remove
    amount = amount.replace("$", "").replace(",", "").strip()

    # TODO: consider error-handling for zero-dollar or negative
    # amounts, which would likely indicate bad data.  This wasn't 
    # specified; for now if empty or a negative provided, we store zero
    if not (amount) or (float(amount) < 0):
        return "0.00"
    else:
        # ensure 2 decimal digits in currency string even if
        # (after rounding) the last digit(s) is/are zero
        amount = "{:.2f}".format(round(float(amount), 2))
    return amount


def is_hardwired(switch_type):
    return switch_type == "Hardwired"


def is_UL_certified(safety_rating):
    return safety_rating == "UL"


def iso_country_code(country):
    try:
        return countries.get(country).alpha3
    except:
        return

def int_or_zero(number):
    try:
        return int(number)
    except ValueError:
        return 0

def bulb_count(bulbs_1, bulbs_2):
    bulbs_1 = int_or_zero(bulbs_1)
    bulbs_2 = int_or_zero(bulbs_2)
    return str(bulbs_1 + bulbs_2)


def format_UPC(UPC):
    # convert 12-digit UPC to 13-digit EAN by padding with leading
    # zero and adding dashes to match the example format provided
    if UPC:
        UPC = "{0:0>13}".format(UPC)
        return UPC[0:3] + "-" + UPC[3:12] + "-" + UPC[12:13]
    else:
        return

def main(args):
    with open("formatted.csv", "w", newline="") as csvfile:
        fieldnames = [
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
            "product__styles",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        with open("homework.csv", "r", newline="") as inputfile:
            reader = csv.DictReader(inputfile)
            for row in reader:


                writer.writerow(
                    {
                        "manufacturer_sku": row["item number"],
                        "ean13": format_UPC(row["upc"]),
                        "weight": row["item weight (pounds)"],
                        "length": row["item depth (inches)"],
                        "width": row["item width (inches)"],
                        "height": row["item height (inches)"],
                        
                        # assumption: if the 'url california label (jpg)'
                        # isn't empty, then prop_65 is True
                        "prop_65": len(row["url california label (jpg)"]) > 0,
                        
                        "cost_price": currency(row["wholesale ($)"]),
                        "min_price": currency(row["msrp ($)"]),
                        # "made_to_order": row["notprovided"],
                        "product__product_class__name": row["item category"],
                        "product__brand__name": row["brand"],
                        "product__title": row["description"],
                        # "product__description": row["long description"],
                        "product__bullets__0": row["selling point 1"],
                        "product__bullets__1": row["selling point 2"],
                        "product__bullets__2": row["selling point 3"],
                        "product__bullets__3": row["selling point 4"],
                        "product__bullets__4": row["selling point 5"],
                        "product__bullets__5": row["selling point 6"],
                        "product__bullets__6": row["selling point 7"],
                        # "product__configuration__codes": row["notprovided"],
                        # "product__multipack_quantity": row["notprovided"],
                        "product__country_of_origin__alpha_3": iso_country_code(row["country of origin"] ),
                        # "product__parent_sku": row["notprovided"],
                        "attrib__arm_height": row["furniture arm height (inches)"],
                        # "attrib__assembly_required": row["notprovided"],
                        # "attrib__back_material": row["notprovided"],
                        # "attrib__blade_finish": row["notprovided"],
                        "attrib__bulb_included": row["bulb 1 included"],
                        "attrib__bulb_type": row["bulb 1 type"],
                        "attrib__color": row["primary color family"],
                        "attrib__cord_length": row["cord length (inches)"],
                        # "attrib__design_id": row["notprovided"],
                        # "attrib__designer": row["notprovided"],
                        "attrib__distressed_finish": "distressed" in row["item finish"].lower(),
                        # "attrib__fill": row["notprovided"],
                        "attrib__finish": row["item finish"],
                        # "attrib__frame_color": row["notprovided"],
                        "attrib__hardwire": is_hardwired(row["switch type"]),
                        # "attrib__kit": row["notprovided"],
                        # "attrib__leg_color": row["notprovided"],
                        # "attrib__leg_finish": row["notprovided"],
                        "attrib__material": row["item materials"],
                        "attrib__number_bulbs": bulb_count( row["bulb 1 count"], row["bulb 2 count"] ),
                        # "attrib__orientation": row["notprovided"],
                        "attrib__outdoor_safe": True if 'yes' in row["outdoor"].lower() else False,
                        # "attrib__pile_height": row["notprovided"],
                        # "attrib__seat_depth": row["notprovided"],
                        "attrib__seat_height": row["furniture seat height (inches)"],
                        # "attrib__seat_width": row["notprovided"],
                        "attrib__shade": row["shade/glass description"],
                        # "attrib__size": row["notprovided"],
                        "attrib__switch_type": row["switch type"],
                        "attrib__ul_certified": is_UL_certified(row["safety rating"]),
                        # "attrib__warranty_years": row["notprovided"],
                        "attrib__wattage": row["bulb 1 wattage"],
                        # "attrib__weave": row["notprovided"],
                        # "attrib__weight_capacity": row["notprovided"],
                        "boxes__0__weight": row["carton 1 weight (pounds)"],
                        "boxes__0__length": row["carton 1 length (inches)"],
                        "boxes__0__height": row["carton 1 height (inches)"],
                        "boxes__0__width": row["carton 1 width (inches)"],
                        "boxes__1__weight": row["carton 2 weight (pounds)"],
                        "boxes__1__length": row["carton 2 length (inches)"],
                        "boxes__1__height": row["carton 2 height (inches)"],
                        "boxes__1__width": row["carton 2 width (inches)"],
                        "boxes__2__weight": row["carton 3 weight (pounds)"],
                        "boxes__2__length": row["carton 3 width (inches)"],
                        "boxes__2__height": row["carton 3 width (inches)"],
                        "boxes__2__width": row["carton 3 width (inches)"],
                        # "boxes__3__weight": row["notprovided"],
                        # "boxes__3__length": row["notprovided"],
                        # "boxes__3__height": row["notprovided"],
                        # "boxes__3__width": row["notprovided"],
                        "product__styles": ", ".join(
                            filter(
                                None,
                                [
                                    row["item style"],
                                    row["item substyle"].replace('/','&'),
                                    row["item substyle 2"].replace('/','&'),
                                ],
                            )
                        ),
                    }
                )
                
        return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))

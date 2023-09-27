def generate_column_mapping(n_boxes: int, n_bullets: int) -> dict[str, str]:
    column_mapping = {
        "item number": "manufacturer_sku",
        "upc": "ean13",
        "item weight (pounds)": "weight",
        "item width (inches)": "width",
        "item depth (inches)": "length",
        "item height (inches)": "height",
        "wholesale ($)": "cost_price",
        "map ($)": "min_price",
        "item category": "product__product_class__name",
        "brand": "product__brand__name",
        "description": "product__title",
        "long description": "product__description",
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
        "max overall height (inches)": "attrib__pile_height",
        "furniture seat height (inches)": "attrib__seat_height",
        "switch type": "attrib__switch_type",
        "safety rating": "attrib__ul_certified",
        "bulb 1 wattage": "attrib__wattage",
        "furniture weight capacity (pounds)": "attrib__weight_capacity",
        "item style": "product__styles"
    }

    # Generate 'product__bullets' mappings
    for i in range(n_bullets):
        column_mapping[f"selling point {i+1}"] = f"product__bullets_{i}"

    # Generate 'boxes' mappings
    for i in range(n_boxes):
        for attribute in ["weight", "length", "height", "width"]:
            column_name = f"carton {i+1} {attribute} (pounds)" if attribute == "weight" else f"carton {i+1} {attribute} (inches)"
            column_mapping[column_name] = f"boxes__{i}__{attribute}"

    return column_mapping


def format_ean13(ean: int) -> str:
    try:
        if ean < 0:
            return None
        ean = str(int(ean)).zfill(12)
    except ValueError:
        return None
    ean13 = f"0{ean[:2]}-{ean[2:11]}-{ean[11]}"
    return ean13

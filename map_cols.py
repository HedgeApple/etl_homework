import pandas as pd


def generate_column_mapping(df: pd.DataFrame) -> dict[str, str]:
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

    bullet_cols = [col for col in df.columns if 'selling point' in col]
    n_bullets = len(bullet_cols)
    for i in range(n_bullets):
        column_mapping[f"selling point {i+1}"] = f"product__bullets__{i}"

    box_cols = [col for col in df.columns if 'carton' in col.split(' ')[0]]
    n_boxes = len(set([col.split(' ')[1] for col in box_cols if len(col.split(' ')) > 1]))
    for i in range(n_boxes):
        for attribute in ["weight", "length", "height", "width"]:
            column_name = f"carton {i+1} {attribute} (pounds)" if attribute == "weight" else f"carton {i+1} {attribute} (inches)"
            if column_name in df.columns:
                column_mapping[column_name] = f"boxes__{i}__{attribute}"

    return column_mapping


def format_ean13(ean: int) -> str:
    try:
        if ean < 0:
            return ""
        ean_str = str(int(ean)).zfill(12)
    except ValueError:
        return ""
    ean13 = f"0{ean_str[:2]}-{ean_str[2:11]}-{ean_str[11]}"
    return ean13


def add_new_columns(df: pd.DataFrame) -> pd.DataFrame:
    new_columns = ["made_to_order", "product__configuration__codes",
                   "product__parent_sku", "attrib__assembly_required",
                   "attrib__back_material", "attrib__blade_finish",
                   "attrib__design_id", "attrib__distressed_finish",
                   "attrib__fill", "attrib__frame_color", "attrib__hardwire",
                   "attrib__leg_color", "attrib__leg_finish",
                   "attrib__orientation", "attrib__seat_depth",
                   "attrib__seat_width", "attrib__shade", "attrib__size",
                   "attrib__warranty_years", "attrib__weave"]

    for column in new_columns:
        df[column] = None
    return df


def column_order() -> list[str]:
    columns = [
        "manufacturer_sku",
        "ean13",
        "weight",
        "length",
        "width",
        "height",
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
        "product__styles"]
    return columns


country_mapping = {
    'China': 'CHN',
    'India': 'IND',
    'Indonesia': 'IDN',
    'Phillipines': 'PH',
    'Thailand': 'TH',
    'Vietnam': 'VN'
}

import pandas as pd


def map_selling_point_columns(df: pd.DataFrame,
                              column_mapping: dict[str, str]) -> None:
    """
    Map the selling point columns in the DataFrame to product bullets.

    Args:
        df (pd.DataFrame): DataFrame to map
        column_mapping (dict[str, str]): The dictionary to store the mapping
        of old column names to new ones.
    """
    bullet_cols = [col for col in df.columns if 'selling point' in col]
    n_bullets = len(bullet_cols)
    for i in range(n_bullets):
        column_mapping[f"selling point {i+1}"] = f"product__bullets__{i}"


def map_carton_columns(df: pd.DataFrame,
                       column_mapping: dict[str, str]) -> None:
    """
    Map the carton columns in the DataFrame to box attributes.

    Args:
        df (pd.DataFrame): DataFrame to map
        column_mapping (dict[str, str]): The dictionary to store the mapping
        of old column names to new ones.
    """
    carton_columns = [
        column for column in df.columns if column.startswith('carton')]
    carton_numbers = [
        column.split(' ')[1] for column in carton_columns if ' ' in column]
    n_boxes = len(set(carton_numbers))
    for i in range(n_boxes):
        for attribute in ["weight", "length", "height", "width"]:
            unit = "(pounds)" if attribute == "weight" else "(inches)"
            column_name = f"carton {i+1} {attribute} {unit}"
            if column_name in df.columns:
                column_mapping[column_name] = f"boxes__{i}__{attribute}"
            else:
                column_name_without_unit = f"carton {i+1} {attribute}"
                if column_name_without_unit in df.columns:
                    column_mapping[
                        column_name_without_unit] = f"boxes__{i}__{attribute}"


def generate_column_mapping(df: pd.DataFrame) -> dict[str, str]:
    """
    Generate a mapping of old column names to new ones.

    Args:
        df (pd.DataFrame): DataFrame

    Returns:
        dict[str, str]: The dictionary that maps old column names to new ones.

    """
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
    try:
        map_selling_point_columns(df, column_mapping)
        map_carton_columns(df, column_mapping)
    except KeyError as key_error:
        print(
            f"Error: DataFrame does not contain expected column: {key_error}")
    except ValueError as ve:
        print(f"Error: column names cannot be converted to an integer.: {ve}")

    return column_mapping


def add_new_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add new columns to the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame

    Returns:
        pd.DataFrame: The DataFrame with added new columns.
    """
    new_columns = ["prop65", "made_to_order", "product__configuration__codes",
                   "product__parent_sku", "attrib__assembly_required",
                   "attrib__back_material", "attrib__blade_finish",
                   "attrib__design_id", "attrib__distressed_finish",
                   "attrib__fill", "attrib__frame_color", "attrib__hardwire",
                   "attrib__leg_color", "attrib__leg_finish",
                   "attrib__orientation", "attrib__seat_depth",
                   "attrib__seat_width", "attrib__shade", "attrib__size",
                   "attrib__warranty_years", "attrib__weave"]

    for column in new_columns:
        df.loc[:, column] = ""
    return df


def column_order() -> list[str]:
    """
    Creates a new order of columns

    Returns:
        list[str]: list of columns
    """
    columns = [
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
        "product__styles"]
    return columns

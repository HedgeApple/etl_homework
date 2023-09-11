from typing import Callable

import pandas as pd

from transformers import (
    currency_transformer, dimension_transformer, country_transformer, boolean_transformer,
    date_transformer
)


class ETL:
    COL_HEADER_MAP = {
        "item number": "manufacturer_sku",
        "upc": "ean13",
        "system creation date": "system_creation_date",
        "item weight (pounds)": "weight",
        "item depth (inches)": "length",
        "item width (inches)": "width",
        "item height (inches)": "height",
        "wholesale ($)": "cost_price",
        "map ($)": "min_price",
        "item category": "product__product_class__name",
        "brand": "product__brand__name",
        "description": "product__description",
        # "long description": "product__description",
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
        "max overall height (inches)": "attrib__pile_height",
        "furniture seat height (inches)": "attrib__seat_height",
        "switch type": "attrib__switch_type",
        "safety rating": "attrib__ul_certified",
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
        "item style": "product__styles",
    }

    @classmethod
    def process_data(cls, dataframe: pd.DataFrame, output_filename: str) -> None:
        """
        Process and transform data then save as `output_filename`

        :param pd.Dataframe dataframe: File read by pandas
        """
        assert isinstance(dataframe, pd.DataFrame), "`dataframe` is not a pandas Dataframe, please validate."

        # Create new file
        output_file = pd.DataFrame()

        for current_col_name, new_col_name in cls.COL_HEADER_MAP.items():
            # Get transformer for column
            transformer = cls.get_transformer_for_column(current_col_name)

            # Apply changes to column with transformer
            output_file[new_col_name] = dataframe[current_col_name].apply(transformer)
            # Save changes
            output_file.to_csv(output_filename, index=False)

    @classmethod
    def get_transformer_for_column(cls, column_name: str) -> Callable | None:
        """
        Get callable formatter method which is going to format column data to required output.
        If no f

        :param str column_name: Name of column
        """
        transformer_map = {
            # Format EAN13 to NNN-...-N format
            "upc": lambda x: str(x)[:3] + "-" + str(x)[3:-1] + "-" + str(x)[-1],
            # Currency columns
            "wholesale ($)": currency_transformer,
            "map ($)": currency_transformer,
            # Dimension columns
            "item weight (pounds)": dimension_transformer,
            "item depth (inches)": dimension_transformer,
            "item width (inches)": dimension_transformer,
            "item height (inches)": dimension_transformer,
            "furniture weight capacity (pounds)": dimension_transformer,
            "carton 1 weight (pounds)": dimension_transformer,
            "carton 1 length (inches)": dimension_transformer,
            "carton 1 height (inches)": dimension_transformer,
            "carton 1 width (inches)": dimension_transformer,
            "carton 2 weight (pounds)": dimension_transformer,
            "carton 2 length (inches)": dimension_transformer,
            "carton 2 height (inches)": dimension_transformer,
            "carton 2 width (inches)": dimension_transformer,
            "carton 3 weight (pounds)": dimension_transformer,
            "carton 3 length (inches)": dimension_transformer,
            "carton 3 height (inches)": dimension_transformer,
            "carton 3 width (inches)": dimension_transformer,
            # Country columns
            "country of origin": country_transformer,
            # Boolean columns
            "conversion kit option": boolean_transformer,
            "outdoor": boolean_transformer,
            # Date columns
            "system creation date": date_transformer
        }

        default_transformer = lambda x: x

        return transformer_map.get(column_name, default_transformer)


if __name__ == "__main__":
    source_file = "homework.csv"
    output_file = "formatted.csv"
    df = pd.read_csv(source_file, dtype="unicode")

    # Start transform
    ETL.process_data(df, output_file)

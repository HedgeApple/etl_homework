import pandas as pd
class ETLPipeline:
    def __init__(
        self, main_dataframe: pd.DataFrame, reference_dataframe: pd.DataFrame
    ) -> None:
        self.main_dataframe = main_dataframe
        self.reference_dataframe = reference_dataframe

    def get_column_name_mapping(self) -> dict:
        """This is the column name mapping 

        Returns:
            dict: column name mapping(main dataframe->reference dataframe)
        """
        return {
            "item number": "manufacturer_sku",
            "upc": "ean13",
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

    def get_country_code(self):
        """This helper function return country code

        Returns:
            _type_: country code mapping
        """
        return {
            "China": "CHN",
            "Indonesia": "IDN",
            "India": "IND",
            "Phillipines": "PHL",
            "Thailand": "THA",
            "Vietnam": "VNM",
        }

    def upc_to_ean13_tranform(self, upc: str) -> str:
        """This helper function converts UPC value to EAN13

        Args:
            upc (str): UPC value 

        Returns:
            str: EAN13 converted value
        """
        return (
            upc[:2] + "-" + upc[2:11] + "-" + upc[-1] if isinstance(upc, str) else upc
        )

    def price_value_transform(self, price_value: str) -> str:
        """This helper function convert price value to expected price value format

        Args:
            price_value (str): price value 

        Returns:
            str: formatted price value
        """
        return (
            "${:,.2f}".format(
                round(float(price_value.replace("$", "").replace(",", "")), 2)
            )
            if isinstance(price_value, str)
            else price_value
        )
    def prop65_transform(self,row)->bool:
        """This function returns whether row indicates prop65 or not

        Args:
            row (_type_): dataframe row

        Returns:
            bool: prop65 
        """
        if pd.isna(row["url california label (jpg)"]) or pd.isna(row["url california label (pdf)"]):
            return False
        else:
            return True
        
        
    def transform(self):
        """This helper function transform input dataframe to expected dataframe

        Returns:
            pd.Dataframe: transformed dataframe
        """
        
        # create new dataframe with all column names of reference dataframe
        flattened_dataframe = self.reference_dataframe[0:0].copy()
        for col_main, col_ref in self.get_column_name_mapping().items():
            flattened_dataframe[col_ref] = self.main_dataframe[col_main]

        # UPC TO EAN13 TRANSFORMATION
        flattened_dataframe["ean13"] = flattened_dataframe["ean13"].astype(str)
        flattened_dataframe["ean13"] = flattened_dataframe["ean13"].apply(
            self.upc_to_ean13_tranform
        )
        # PRICE TRANSFORMATION
        flattened_dataframe[["cost_price", "min_price"]] = flattened_dataframe[
            ["cost_price", "min_price"]
        ].applymap(self.price_value_transform)

        # California Proposition 65 TRANSFORMATION
        flattened_dataframe["prop_65"] = self.main_dataframe.apply(self.prop65_transform, axis=1)

        # Country of origin TRANSFORMATION
        flattened_dataframe[
            "product__country_of_origin__alpha_3"
        ] = flattened_dataframe["product__country_of_origin__alpha_3"].replace(
            self.get_country_code(), regex=True
        )

        # Converting YES and NO/None values to True and False
        flattened_dataframe[
            ["attrib__bulb_included", "attrib__outdoor_safe"]
        ] = flattened_dataframe[
            ["attrib__bulb_included", "attrib__outdoor_safe"]
        ].apply(
            lambda x: True if str(x).lower() == "yes" else False
        )

        # UL Certification Transformation
        flattened_dataframe["attrib__ul_certified"] = flattened_dataframe[
            "attrib__ul_certified"
        ].apply(lambda x: True if "ul" in str(x).lower() else False)
        return flattened_dataframe
    def __call__(self) -> bool:
        flattened_dataframe = self.transform()
        # export dataframe 
        flattened_dataframe.to_csv("formatted.csv",index=False)
        return True

if __name__ == "__main__":
    # read csv homework data
    homework_dataframe = pd.read_csv("./homework.csv", dtype="unicode")
    example_dataframe = pd.read_csv("./example.csv")
    # etl class object
    etl_pipeline = ETLPipeline(
        main_dataframe=homework_dataframe, reference_dataframe=example_dataframe
    )
    print(f"ETL Pipeline successful: {etl_pipeline()}")

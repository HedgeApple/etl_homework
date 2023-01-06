import pandas as pd
import numpy as np
import pycountry

###kindly refer to the nookbook to completely understand the transformation code


class Transformer(object):
    def __init__(self, input_file_path, output_file_path="formatted.csv"):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.df = pd.read_csv("homework.csv", low_memory=False)

    def parser(self):
        """Transform the data"""
        self.df["system creation date"] = pd.to_datetime(
            self.df["system creation date"], format="%m/%d/%y"
        ).dt.strftime("%Y-%m-%d")

        for i in self.df.columns:
            if "$" in i:
                self.df[i] = self.df.apply(
                    lambda row: self.process_money(row[i]), axis=1
                )
                self.df[i] = self.df[i].apply(
                    lambda x: round(x, 2) if pd.notnull(x) else x
                )

        for col in self.df.columns:
            if "feet" in col:
                self.df[col] = self.df[col].apply(self.cubic_feet_to_inches)
                self.df.rename(
                    columns={col: col.replace("feet", "inches")}, inplace=True
                )

        for col in self.df.columns:
            for i in range(1, 4):
                for k in ["width", "length", "height", "weight", "volume"]:
                    j = f"{i} {k}"
                    if j in col:
                        # print("boxes__"+str(i-1)+"__"+k)
                        self.df.rename(
                            columns={col: f"boxes__{i - 1}__{k}"}, inplace=True
                        )

        # we had an exceptional case, that wasnt in a generic form

        # in this case we had an exception of "Philippines" and "Viet Nam"
        # as their names were misspelled in the original document
        self.df["country of origin"] = self.df["country of origin"].replace(
            ["Phillipines", "Vietnam"], ["Philippines", "Viet Nam"]
        )
        self.df["country of origin"] = self.df["country of origin"].fillna(
            "temp"
        )  ##temp value, to be replaced afterwards
        self.df["country of origin"].apply(lambda x: self.Country_to_alpha_3(x))

        # replacing the word "item" by "product" as shown in the example.csv
        self.df.columns = [c.replace("item", "product") for c in list(self.df.columns)]

        self.df.rename(
            columns={
                "carton2volumecubicinches": f"boxes__{2}__volume",
                "country of origin": "product__country_of_origin__alpha_3",
                "description": "product__description",
                "brand": "product__brand__name",
                "item category": "product__product_class__name",
            },
            inplace=True,
        )

        # in the example.csv file, some of the columns had the word "Attrib" in the beginning,
        # i according to my understanding, added this word to some column names
        l = self.df.columns.get_loc("bulb 1 count")
        h = self.df.columns.get_loc("furniture weight capacity (pounds)")

        for i in range(l, h + 1):
            self.df.rename(
                columns={self.df.columns[i]: "attrib " + self.df.columns[i]},
                inplace=True,
            )

        # adding "__" between the words in column names to match the "example.csv" format
        for col in self.df.columns:
            k = col.split(" ")
            if len(k) > 1:
                self.df.rename(columns={col: "__".join(k)}, inplace=True)

        self.df["upc"] = self.df["upc"].astype(str)
        self.export_csv()

    @staticmethod
    def process_money(money):
        """Normalize and process money to float datatype

        Args:
            money (obj): _description_

        Returns:
            float: _description_
        """
        if type(money) == float:
            return money
        elif type(money) == int:
            return float(money)
        elif type(money) == str:
            return float(money.strip().replace("$", "").replace(",", "").strip())

    @staticmethod
    def cubic_feet_to_inches(cubic_feet):
        """convert cubic_feet to inches

        Args:
            cubic_feet (float): _description_

        Returns:
            float: cubic_feet converted into inches
        """
        inches = cubic_feet * 12**3
        return inches

    @staticmethod
    def Country_to_alpha_3(x):
        """Get Country alpha3 code

        Args:
            x (str): Country Name

        Returns:
            str: returns country alpha_3 code

        Example:
            Arg: "China"
            Returns: "CHN" or None
        """
        if not pycountry.countries.get(name=x):
            return np.nan
        else:
            return pycountry.countries.get(name=x).alpha_3

    def export_csv(self):
        """Export DataFrame to csv"""
        self.df.to_csv(self.output_file_path)

    def print_df(self):
        """print dataFrame"""
        pd.set_option("display.max_columns", 146)
        pd.set_option("display.max_rows", 10)
        print(self.df)


if __name__ == "__main__":
    input_filepath = "homework.csv"
    output_filepath = "formatted.csv"
    Transformer(input_filepath, output_filepath).parser()

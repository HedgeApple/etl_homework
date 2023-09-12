from datetime import datetime


class transforms:

    def get_returned_obj(
        self,
        obj=None
    ):
        if obj:
            return obj
        else:
            return obj

    # ------------------------------------------

    def date_transform(
        self,
        date=None,
    ):
        if date:
            cleaned_date = date.replace(" ", "")

            last_value = cleaned_date.split("/")[-1]
            
            if len(last_value) == 4:
                date_obj = datetime.strptime(cleaned_date, "%d/%m/%Y").date()
            elif len(last_value) == 2:
                date_obj = datetime.strptime(cleaned_date, "%m/%d/%y").date()
        else:
            date_obj = None
        
        return self.get_returned_obj(obj=date_obj)
    
    # ------------------------------------------

    def upc_transform(
        self, 
        upc=None,
    ):
        if upc:
            if isinstance(upc, (float, int)):
                upc_obj = str(upc)
            elif isinstance(upc, (str)):
                upc_cleaned = upc.replace(" ", "")
                if not upc_cleaned:
                    upc_obj = None
                else:
                    upc_obj = upc.replace(" ", "")
        else:
            upc_obj = None
        
        return self.get_returned_obj(obj=upc_obj)
    
    # ------------------------------------------
    
    def currency_transfrom(
        self,
        currency=None,
    ):
        if currency:
            if isinstance(currency, (float, int)):
                currency_obj = "{0:.2f}".format(currency)
            elif isinstance(currency, str):
                currency_cleaned = currency.replace("$", "").replace(" ", "").replace(",", "")
                currency_obj = "{0:.2f}".format(float(currency_cleaned))
        else:
            currency_obj = None
        
        return self.get_returned_obj(obj=currency_obj)
    
    # ------------------------------------------

    def dimension_transform(
        self,
        dimension=None
    ):
        pass
        
    # ------------------------------------------

    def weight_transform(
        self,
        weight=None
    ):
        pass
        
# ----------------------------------------------------------------------
# End of File
# ----------------------------------------------------------------------
            
    
from geomeppy import IDF
from case_edits.epcase import EneryPlusCaseEditor

class OutputRequests:
    def __init__(self, epcase:EneryPlusCaseEditor) -> None:
        self.epcase = epcase

    def add_output_variable(self, name:str, reporting_frequency="Timestep"):
        if self.check_existing_variable(name):
            return 
        
        obj =  self.epcase.idf.newidfobject("OUTPUT:VARIABLE")
        obj.Key_Value = "*"
        obj.Variable_Name = name
        obj.Reporting_Frequency = reporting_frequency


    def request_sql(self):
        if not self.epcase.idf.idfobjects["OUTPUT:SQLITE"]:
            obj = self.epcase.idf.newidfobject("OUTPUT:SQLITE")
            obj.Option_Type = "Simple" 


    def request_json(self):
        if not self.epcase.idf.idfobjects["OUTPUT:JSON"]:
            obj = self.epcase.idf.newidfobject("OUTPUT:JSON")
            obj.Option_Type = "TimeSeries" 


    def check_existing_variable(self, new_var_name):
        var_names = [o.Variable_Name  for o in self.epcase.idf.idfobjects["OUTPUT:VARIABLE"]]
        if new_var_name in var_names:
            print(f"`{new_var_name}` is already in IDF")
            return True


    
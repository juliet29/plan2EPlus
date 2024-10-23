from re import L
from geomeppy import IDF
from helpers.variable_interfaces import all_variables, get_vars


def check_existing_variable(idf: IDF, new_var_name):
    var_names = [o.Variable_Name for o in idf.idfobjects["OUTPUT:VARIABLE"]]
    if new_var_name in var_names:
        # print(f"`{new_var_name}` is already in IDF") TODO log
        return True


def is_surface_or_zone_wind(name):
    if "Wind" in name:
        if "Zone" in name or "Surace" in name:
            return True

def add_output_variable(idf: IDF, name: str, reporting_frequency="Timestep"):
    if check_existing_variable(idf, name):
        return idf
    
    if is_surface_or_zone_wind(name):
        reporting_frequency = "Hourly"

    obj = idf.newidfobject("OUTPUT:VARIABLE")
    obj.Key_Value = "*"
    obj.Variable_Name = name
    obj.Reporting_Frequency = reporting_frequency
    return idf


def request_sql(idf: IDF):
    if not idf.idfobjects["OUTPUT:SQLITE"]:
        obj = idf.newidfobject("OUTPUT:SQLITE")
        obj.Option_Type = "Simple"

    return idf


def request_dxf(idf: IDF):
    var = "Output:Surfaces:Drawing".upper()
    if not idf.idfobjects[var]:
        obj = idf.newidfobject(var)
        obj.Report_Type = "DXF"
    return idf


def request_advanced_variables(idf: IDF):
    obj = idf.newidfobject("OUTPUT:DIAGNOSTICS")
    obj.Key_1 = "DisplayAdvancedReportVariables"
    return idf


def add_all_output_requests(idf:IDF):
    idf = request_sql(idf)
    idf = request_dxf(idf)
    idf = request_advanced_variables(idf)

    vars = get_vars([all_variables.afn, all_variables.zone, all_variables.site])

    for var in vars:
        idf = add_output_variable(idf, var)
    return idf

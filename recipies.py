from helpers import *

def add_output_variable(idf:IDF, name, reporting_frequency="Timestep"):
    # see https://bigladdersoftware.com/epx/docs/23-2/input-output-reference/input-for-output.html#outputvariable
    idf.newidfobject("OUTPUT:VARIABLE")

    obj = idf.idfobjects["OUTPUT:VARIABLE"][-1]
    obj.Key_Value = "*"
    obj.Variable_Name = name
    obj.Reporting_Frequency = reporting_frequency

    return idf

    
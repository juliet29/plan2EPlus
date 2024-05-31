from geomeppy import IDF

def add_output_variable(idf:IDF, name, reporting_frequency="Timestep"):
    # see https://bigladdersoftware.com/epx/docs/23-2/input-output-reference/input-for-output.html#outputvariable
    idf.newidfobject("OUTPUT:VARIABLE")

    obj = idf.idfobjects["OUTPUT:VARIABLE"][-1]
    obj.Key_Value = "*"
    obj.Variable_Name = name
    obj.Reporting_Frequency = reporting_frequency

    return idf

def request_sql(idf:IDF, ):
    # https://bigladdersoftware.com/epx/docs/23-2/input-output-reference/input-for-output.html#outputsqlite
    idf.newidfobject("OUTPUT:SQLITE")

    obj = idf.idfobjects["OUTPUT:SQLITE"][0]
    obj.Option_Type = "Simple" 

    return idf


def request_json(idf:IDF, ):
    #https://bigladdersoftware.com/epx/docs/23-2/input-output-reference/input-for-output.html#outputjson
    idf.newidfobject("OUTPUT:JSON")

    obj = idf.idfobjects["OUTPUT:JSON"][0]
    obj.Option_Type = "TimeSeries" 

    return idf

    
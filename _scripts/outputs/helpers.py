from ladybug.analysisperiod import AnalysisPeriod
from enum import Enum

def create_plot_title(dataset):
    variable = dataset.header.metadata["type"]
    unit = dataset.header.unit
    analysis_period = str(dataset.header.analysis_period)
    title = f"{variable} [{unit}] <br><sup> {analysis_period} </sup>"
    return title


def create_analysis_period(ap_dict):
    # TODO just need ap shorthand.. 
    ap_dict.pop("type")
    ap = AnalysisPeriod(**ap_dict)
    ap_name = f"{ap.st_month}-{ap.st_day}"
    return ap, ap_name



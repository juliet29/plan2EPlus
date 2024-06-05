import os
from ladybug.sql import SQLiteResult
from ladybug.analysisperiod import AnalysisPeriod

from case_edits.epcase import EneryPlusCaseReader
from geometry.geometry_parser import GeometryParser

from outputs.variables import OutputVars
from outputs.classes import GeometryOutputData


def create_analysis_period(ap_dict):
    ap_dict.pop("type")
    ap = AnalysisPeriod(**ap_dict)
    ap_name = f"{ap.st_month}-{ap.st_day}"
    return ap, ap_name


class SQLReader:
    def __init__(self, CASE_NAME) -> None:
        self.case_name = CASE_NAME
        self._get_sql_outputs()
        self._get_geometry()

        self.dataset_names = []
        self._match_geom_sql()

    def _get_sql_outputs(
        self,
    ):
        SQL_PATH = os.path.join("cases", self.case_name, "results", "eplusout.sql")
        self.sqld = SQLiteResult(SQL_PATH)

    def _get_geometry(self):
        self.epcase = EneryPlusCaseReader(self.case_name)
        geo = GeometryParser(self.epcase.idf)
        geo.get_zones()
        self.zone_dict = {i.name.upper(): i for i in geo.zones}
        self.zone_list = geo.zones

    def _match_geom_sql(self, output_var=OutputVars.zone_mean_air_temp):
        self.collection = self.sqld.data_collections_by_output_name(output_var.value)

        for dataset in self.collection:
            ap, ap_name = create_analysis_period(
                dataset.header.to_dict()["analysis_period"]
            )
            dataset_name = f"{output_var.name}{ap_name}"
            out_data = GeometryOutputData(dataset, ap, dataset_name)

            zone_name = dataset.header.to_dict()["metadata"]["Zone"]
            self.zone_dict[zone_name].create_output_data(out_data)

            if dataset_name not in self.dataset_names:
                self.dataset_names.append(dataset_name)

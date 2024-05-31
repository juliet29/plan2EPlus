from ladybug.sql import SQLiteResult

from outputs.output_var_names import OutputVariables

class SQLReader:
    def __init__(self, SQL_PATH) -> None:
        self.sqld = SQLiteResult(SQL_PATH)
        pass

    def get_zone_data(self, index):
        # TODO assert that this data is at the zone level 
        self.collection = self.sqld.data_collections_by_output_name(OutputVariables.zone_mean_air_temp.value)

        zone = self.collection[index].header.to_dict()["metadata"]["Zone"]
        dates = self.collection[index].datetimes
        vals = self.collection[index].values 
        


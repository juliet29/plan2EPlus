from ladybug.sql import SQLiteResult


from outputs.output_names import OutputVariables
from outputs.output_data import OutputData

class SQLReader:
    def __init__(self, SQL_PATH) -> None:
        self.sqld = SQLiteResult(SQL_PATH)
        self.data = {}


    def get_zone_data(self, index):
        # TODO assert that this data is at the zone level 
        self.collection = self.sqld.data_collections_by_output_name(OutputVariables.zone_mean_air_temp.value)

        zone_name = self.collection[index].header.to_dict()["metadata"]["Zone"]
        times = self.collection[index].datetimes
        values = self.collection[index].values 
        self.data[index] = OutputData(zone_name, times, values)

        # TODO use are_collections_aligned(data_collections, raise_exception=True) to check => only want to look at data for one analysis period ..

    def prepare_spatial_data(self, time_indices):
        # TODO => map times to indices ..

        self.spatial_data = {}
        self.spatial_times = []
        self.spatial_values = []
        for time_ix in time_indices:
            self.spatial_data[time_ix] = []
            for ix, val in enumerate(self.data.values()):
                value = round(val.values[time_ix],3)
                self.spatial_data[time_ix].append((val.name, value))
                self.spatial_values.append(value)
                if ix == 0:
                    self.spatial_times.append(val.times[time_ix])

            



        

        


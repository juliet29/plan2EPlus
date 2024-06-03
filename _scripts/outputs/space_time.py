from outputs.sql import SQLReader
from outputs.output_data import TimeExtractData
# from datetime import time

from helpers.helpers import min_max_norm
from helpers.plots import get_norm_plotly_colors, create_colorbar

class SpaceTimePlot(SQLReader):
    def __init__(self, CASE_NAME) -> None:
        super().__init__(CASE_NAME)


    def extract_many_times(self, times, dataset_name):
        # TODO should be init vars..
        self.dataset_name = dataset_name
        self.candidate_times = times
        self.get_dataset_datetimes()
        self.get_time_indices()
         
        for ix in self.time_indices:
            self.extract_time_data(ix)

    def get_time_indices(self):
        self.time_indices = []
        for candidate_time in self.candidate_times:
            self.check_valid_time(candidate_time)

    def check_valid_time(self, candidate_time):
        for ix, datetime in enumerate(self.datetimes):
            if candidate_time == datetime.time:
                self.time_indices.append(ix)
                return 
        raise Exception(f"{candidate_time} is an invalid time. There is a {self.timestep}!!")


    def extract_time_data(self, time_index):
        self.spatial_values = []
        for zone in self.zone_dict.values():
            value = zone.output_data[self.dataset_name].dataset.values[time_index]
            self.spatial_values.append(value)

            data = TimeExtractData(value, time_index)
            zone.create_extracted_data(self.dataset_name, data)
            

    def prepare_spatial_colors(self, dataset_name):
        min_val = min(self.spatial_values)
        max_val = max(self.spatial_values)
        for zone in self.zone_dict.values():
            val = zone.extracted_data[dataset_name].value
            norm_val = min_max_norm(val, min_val, max_val)
            color = get_norm_plotly_colors(norm_val, min_val, max_val)[0]
            zone.color_extracted_data(dataset_name, color)

        self.colorbar_trace = create_colorbar(min_val, max_val)


    def get_dataset_datetimes(self):
        dataset = self.zone_list[0].output_data[self.dataset_name].dataset
        self.datetimes = dataset.datetimes
        self.timestep = dataset.timestep_text

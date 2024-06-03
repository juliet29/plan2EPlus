class OutputData:
    def __init__(self, name, times, values) -> None:
        self.name = name
        self.times = times
        self.values = values
        # TODO can use to validate 
        # self.data_type
        # self.analysis_period
        pass

    def __repr__(self):
        return f"OutputData({self.name})"  
    


class GeometryOutputData:
    def __init__(self, dataset, analysis_period, short_name) -> None:
        self.dataset = dataset
        self.analysis_period = analysis_period
        self.short_name = short_name
        # self.times = times
        # self.values = values
        # TODO can use to validate 
        # self.data_type
        # self.analysis_period

    def __repr__(self):
        return f"OutputData({self.short_name})"  
    

class TimeExtractData:
    def __init__(self, value, index) -> None:
        self.value = value
        self.index = index 

    def __repr__(self):
        return f"TimeExtractData({self.index})"  

    def update_color(self, color):
        self.color = color
class SiteData:
    def __init__(self, dataset, type, unit) -> None:
        self.dataset = dataset
        self.type = type
        self.unit = unit
  

    def __repr__(self):
        return f"OutputData({self.dataset})"  
    


class GeometryOutputData:
    def __init__(self, dataset, analysis_period, short_name, analysis_period_name) -> None:
        self.dataset = dataset
        self.analysis_period = analysis_period
        self.short_name = short_name
        self.analysis_period_name = analysis_period_name

        self.properties()

    def properties(self):
        self.formal_name = self.dataset.header.to_dict()["metadata"]["type"]
        self.unit = self.dataset.header.to_dict()["unit"]


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
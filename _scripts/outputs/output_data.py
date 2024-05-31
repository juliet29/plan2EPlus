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
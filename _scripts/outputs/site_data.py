import plotly.graph_objects as go
from plotly.subplots import make_subplots


from outputs.output_names import OutputVariables
from outputs.output_data import SiteData
from outputs.sql import SQLReader, create_analysis_period


class SiteDataPlots(SQLReader):
    def __init__(self, CASE_NAME) -> None:
        super().__init__(CASE_NAME)
        self.site_data = {}
        self.analysis_period_names = []
        self.outputs = []

    def get_site_name(self):
        self.site_name = self.epcase.idf.idfobjects["SITE:LOCATION"][0].Name

    def update_site_data(self, output_var):
        if output_var not in self.outputs:
            self.outputs.append(output_var)

        collection = self.sqld.data_collections_by_output_name(output_var.value)
        # TODO assert zone in environment using to_dict()
        self.site_data[output_var.name] = {}

        for dataset in collection:
            data_object, ap_name = self.create_data_object(dataset)
            self.site_data[output_var.name][ap_name] = data_object


    def create_data_object(self, dataset):
        header =  dataset.header.to_dict()
        _, ap_name = create_analysis_period(header["analysis_period"])
        if ap_name not in self.analysis_period_names:
            self.analysis_period_names.append(ap_name)


        data_type = header["data_type"]["name"]
        unit = header["unit"]
        return SiteData(dataset, data_type, unit), ap_name
    

    def plot_site_data(self, var, ap_index):
        assert var.name in self.site_data.keys()

        analysis_period = self.analysis_period_names[ap_index]
        assert analysis_period in self.analysis_period_names

        data = self.site_data[var.name][analysis_period]
        dataset = data.dataset

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dataset.datetimes, y=dataset.values))

        fig.update_xaxes(title_text='Time')
        fig.update_yaxes(title_text=f"{data.type} [{data.unit}]")
        fig.update_layout(title_text=f"{analysis_period} {var.value}")

        return fig
    
    def plot_all_site_data(self, ap_index):
        self.get_site_name()

        analysis_period = self.analysis_period_names[ap_index]
        assert analysis_period in self.analysis_period_names

        output_names = [v.value for v in self.outputs]
        fig = make_subplots(
            rows=len(self.outputs), cols=1, subplot_titles=output_names,
            shared_xaxes=True,
        )

        for ix, output in enumerate(self.site_data.values()):
            data = output[analysis_period]
            dataset = data.dataset
            fig.add_trace(go.Scatter(x=dataset.datetimes, y=dataset.values), row=ix+1, col=1)
            fig.update_yaxes(title_text=f"{data.type} [{data.unit}]", row=ix+1, col=1)

        fig.update_layout(title_text=f"{analysis_period} {self.site_name}", showlegend=False)

        return fig











    

    
            

from ladybug.datacollection import BaseCollection
import plotly.graph_objects as go



def get_name_for_spatial_data(dataset: BaseCollection):
    keys = dataset.header.metadata.keys()
    for i in ["System", "Zone", "Surface"]:
        if i in keys:
            return dataset.header.metadata[i]
    else:
        raise Exception("Spatial type is not defined")


def create_plot_title(dataset: BaseCollection):
    variable = dataset.header.metadata["type"]
    unit = dataset.header.unit
    analysis_period = str(dataset.header.analysis_period)
    title = f"{variable} [{unit}] <br><sup> {analysis_period} </sup>"
    return title


def line_plot(collections: list[BaseCollection]):
    fig = go.Figure()

    for dataset in collections:
        name = get_name_for_spatial_data(dataset)
        fig.add_trace(go.Scatter(x=dataset.datetimes, y=dataset.values, name=name))

    title = create_plot_title(dataset)
    fig.update_layout(title_text=title)

    return fig




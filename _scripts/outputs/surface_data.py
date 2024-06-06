import plotly.graph_objects as go

from outputs.sql import SQLReader

class SurfaceData(SQLReader):
    def __init__(self, CASE_NAME) -> None:
        super().__init__(CASE_NAME)
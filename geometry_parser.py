from geomeppy import IDF
from geomeppy.patches import EpBunch

import fnmatch
import re

import shapely as sp
from helper_classes import *
from icecream import ic


class GeometryParser:
    def __init__(self, idf) -> None:
        self.idf = idf

    def run(self):
        self.get_zones()



    def get_zones(self):
        self.zones = [Zone(i) for i in self.idf.idfobjects["ZONE"]]


    def get_walls(self, zone:Zone, expected_walls=4):
        # walls are differentiated from floors / cielings because they have 2 different z values within their coordinates.
        all_surfaces = self.idf.idfobjects["BUILDINGSURFACE:DETAILED"]
        zone_surfaces = [
            surface for surface in all_surfaces if surface.Zone_Name == zone.name
        ]

        for surface in zone_surfaces:
            # get fieldnames for the z coordinates
            valid_fieldnames = fnmatch.filter(
                surface.fieldnames, f"Vertex_[0-{expected_walls}]_Zcoordinate"
            )

            # check that we have 2 different z coordinates
            valid_values = []
            for fieldname in valid_fieldnames:
                valid_values.append(surface[fieldname])
            if len(set(valid_values)) == 2:
                zone.walls.append(Wall(surface))

        assert len(zone.walls) == expected_walls, "Added walls != expected walls"
        

    def get_wall_geometry(self, wall:Wall):
        z_coords = fnmatch.filter(wall.data.fieldnames, "Vertex_[0-4]_Zcoordinate")

        # Define the regex pattern to match digits
        pattern = re.compile(r"\d+")

        vertices = []
        for fieldname in z_coords:
            if wall.data[fieldname] == 0:
                # get the vertex number where z-coord is 0
                matches = pattern.findall(fieldname)
                # TODO some tests needed here..
                x_field = fnmatch.filter(
                    wall.data.fieldnames, f"Vertex_{matches[0]}_Xcoordinate"
                )[0]
                x_val = wall.data[x_field]

                y_field = fnmatch.filter(
                    wall.data.fieldnames, f"Vertex_{matches[0]}_Ycoordinate"
                )[0]
                y_val = wall.data[y_field]

                vertices.append([x_val, y_val])

        wall.line = sp.LineString(vertices)
       

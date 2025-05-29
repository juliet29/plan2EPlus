# plot nodes and labels..
from pathlib import Path
from typing import Optional
from geomeppy import IDF

import networkx as nx
from ...helpers.helpers import set_union
from ...helpers.ep_helpers import (
    get_partner_of_surface,
    get_subsurface_by_name,
    get_subsurface_wall_num,
    get_surface_by_name,
)
from .cardinal_positions import create_cardinal_positions, NodePositions
from ...plan.graph_to_subsurfaces import get_subsurface_pairs_from_case
from ...plan.helpers import create_room_map
from ...helpers.ep_helpers import get_surface_direction, get_zones, WallNormal
from ...helpers.ep_geom_helpers import create_domain_for_zone
from ...subsurfaces.interfaces import SubsurfacePair
from ...subsurfaces.logic import get_connecting_surface
from typing import NamedTuple, TypedDict, Literal


class EdgeDetails(TypedDict):
    surface: str
    subsurfaces: str
    stype: Literal["WINDOW", "DOOR"]


class GraphEdge(NamedTuple):
    source: str
    target: str
    details: EdgeDetails


def create_graph_for_zone(idf: IDF, path_to_input: Path):
    G = nx.DiGraph()
    positions = {}
    room_map = create_room_map(path_to_input)

    # node should have num and label

    for ix, zone in enumerate(get_zones(idf)):
        room_name = room_map[ix]
        label = f"{ix}-{room_name}"
        G.add_node(label, num=ix, room_name=room_name, zone_name=zone.Name)
        positions[label] = create_domain_for_zone(idf, ix).centroid.pair
        # positions
    return G, positions


def add_cardinal_directions(G: nx.DiGraph, positions: NodePositions):
    for i in WallNormal:
        G.add_node(i.name, type="Direction", zone_name=i.name)
    new_positions = create_cardinal_positions(positions)
    return G, new_positions


def filter_nodes(G: nx.DiGraph):
    # TODO redo! zone_name in [i.name for i in WallNormal] or not..
    zone_nodes = [i[0] for i in G.nodes(data=True) if "zone_name" in i[1].keys()]
    cardinal_nodes = [i[0] for i in G.nodes(data=True) if "zone_name" in i[1].keys()]
    return zone_nodes, cardinal_nodes


def get_partners_of_surface_or_subsurface(idf: IDF, name: str):
    name = name.title()
    try:
        subsurf_obj = get_subsurface_by_name(idf, name)
        assert subsurf_obj, f"No suburface found for {name}"
        surf = get_surface_by_name(idf, subsurf_obj.Building_Surface_Name)
    except:
        surf = get_surface_by_name(idf, name)

    assert surf, f"No surface found for {name}"
    space_a = surf.Zone_Name

    if surf.Outside_Boundary_Condition == "outdoors":
        surf_dir = get_surface_direction(idf, surf.Name)
        space_b = surf_dir.name
    else:
        partner_surf = get_partner_of_surface(idf, surf)
        assert partner_surf
        space_b = partner_surf.Zone_Name

    return space_a, space_b


def get_node_in_G(G: nx.DiGraph, zone_name: str):
    for node in G.nodes:
        if G.nodes[node].get("zone_name") == zone_name:
            return node
    raise Exception(f"No node found for zone_name:`{zone_name}` in G.nodes: {G.nodes}")


def get_node_partners(idf: IDF, G: nx.DiGraph, surf_name: str):
    partners = get_partners_of_surface_or_subsurface(idf, surf_name)
    nodes = [get_node_in_G(G, i) for i in partners]
    return nodes


def add_edges(idf: IDF, G: nx.DiGraph):
    # not using AFN linkages because some subsurfaces might not be linkages..
    all_subsurf = [i.Name for i in idf.getsubsurfaces() if "Partner" not in i.Name]
    afn_surfaces = [
        i.Surface_Name for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
    ]
    all_poss_surfs = set_union(all_subsurf, afn_surfaces)

    for s in all_poss_surfs:
        nodes = get_node_partners(idf, G, s)
        G.add_edge(*nodes, surface=s)

    return G


def create_base_graph(idf: IDF, path_to_input: Path):
    G, positions = create_graph_for_zone(idf, path_to_input)
    G, positions = add_cardinal_directions(G, positions)
    G = add_edges(idf, G)
    return G, positions


## TODO -- this goes elsewhere -------


def create_edge_label(G: nx.DiGraph, edge: GraphEdge):
    def map_ss_type(val):
        d = {"DOOR": "DR", "WINDOW": "WND"}
        return d[val]

    owning_zone = G.nodes[edge.source]["num"]
    type = map_ss_type(edge.details["stype"])
    wall_num = get_subsurface_wall_num(edge.details["subsurfaces"])

    return f"{type}-{owning_zone}-{wall_num}"


def create_edge_label_dict(G: nx.DiGraph):
    nice_edges = [GraphEdge(*e) for e in G.edges(data=True)]
    return {(e.source, e.target): create_edge_label(G, e) for e in nice_edges}


## -- ^^^ this goes elsewhere -------


def create_multi_graph(G: nx.DiGraph):
    G_rev = G.reverse()
    for e in G_rev.edges:
        G_rev.edges[e]["reverse"] = True
    Gm = nx.MultiDiGraph(G, G_rev)

    return Gm


def init_multigraph(idf: IDF, path_to_input: Path):
    G, pos = create_base_graph(idf, path_to_input)
    Gm = create_multi_graph(G)
    return Gm, pos


def create_afn_graph(idf: IDF, G: nx.DiGraph):
    def is_node_afn_zone(node):
        afn_zones = [
            i.Zone_Name for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]
        ]
        return G.nodes[node].get("zone_name") in afn_zones

    def is_edge_afn_surface(e):
        afn_surfaces = [
            i.Surface_Name for i in idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
        ]
        return G.edges[e].get("subsurfaces") in afn_surfaces

    nodes = [n for n in G.nodes if is_node_afn_zone(n)]
    G_zones = nx.subgraph(G, nodes)

    edges = [e for e in G.edges if is_edge_afn_surface(e)]
    G_afn = nx.edge_subgraph(G, edges)

    assert G_zones.nodes < G_afn.nodes, (
        "Graph induced on subsurfaces should include all AFN zones"
    )

    return G_afn

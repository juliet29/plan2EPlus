from geomeppy import IDF
import networkx as nx
import matplotlib.pyplot as plt

from .network import create_afn_graph, create_edge_label_dict, filter_nodes


NODE_COLOR = "#99d3ff"
CARDINAL_COLOR = "#ffec99"
DEFAULT_EDGE = "#000000"

GREYED_OUT_NODE = "#E5D4ED"
GREYED_OUT_EDGE = "#DFDFE2"

BRIGHT_NODE = "#ed6904"
BRIGHT_NODE2 = "#ad6804"


def draw_graph_with_node_labels(
    G, pos, nodes, color=NODE_COLOR, shape="s", alpha=0.5, size=500
):
    margin = 0.001
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=nodes,
        margins=(margin, margin),
        node_shape=shape,
        node_color=color,
        alpha=alpha,
        node_size=size,
    )
    labels = {n: n for n in nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    # nx.draw_networkx_edges(G, pos, arrows=True)


def draw_graph_edges_with_labels(G, pos, label_dict, color=DEFAULT_EDGE):
    nx.draw_networkx_edges(G, pos, edge_color=color)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=label_dict, font_color=color)


def draw_over(G, pos, color, label_dict):
    nx.draw_networkx_nodes(G, pos, node_color=color)
    nx.draw_networkx_edges(G, pos, edge_color=color)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=label_dict, font_color=color)


def draw_init_graph(
    G, positions, node_color=GREYED_OUT_NODE, edge_color=GREYED_OUT_EDGE
):
    zone_nodes, cardinal_nodes = filter_nodes(G)
    e_labels = create_edge_label_dict(G)

    fig = plt.figure(3, figsize=(12, 8))

    draw_graph_with_node_labels(G, positions, zone_nodes, color=node_color)
    draw_graph_with_node_labels(
        G, positions, cardinal_nodes, color=node_color, shape="*", size=400
    )
    draw_graph_edges_with_labels(G, positions, e_labels, color=edge_color)

    return fig


def draw_afn_graph(G, fig, positions, color=BRIGHT_NODE):
    e_labels = create_edge_label_dict(G)
    draw_over(G, positions, color, e_labels)
    return fig


def draw_afn_over_init(G, G_afn, positions):
    fig = draw_init_graph(G, positions)
    fig = draw_afn_graph(G_afn, fig, positions)

    return fig

import networkx as nx


NODE_COLOR = "#99d3ff"
CARDINAL_COLOR = "#ffec99"


def draw_graph_with_node_labels(
    G, pos, nodes, color=NODE_COLOR, shape="s", alpha=0.5, size=300
):
    margin = 0.1
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
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7)

    # nx.draw_networkx_edges(G, pos, arrows=True)

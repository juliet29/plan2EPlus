import networkx as nx


def draw_graph_with_node_labels(
    G,
    pos,
):
    nx.draw(G, pos=pos)
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G}, font_size=10)

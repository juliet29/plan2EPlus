import polars as pl
import networkx as nx


def normalize_to_target(arr:pl.Series, t_min=0, t_max=1):
    # log scale might be better..
    r_min, r_max = arr.min(), arr.max()
    normalize = lambda x: (x - r_min) / (r_max - r_min) # type: ignore
    scale = lambda x: (normalize(x) * (t_max - t_min)) + t_min
    return [scale(i) for i in arr]

def get_matching_edge(G:nx.DiGraph ,subsurface_name:str):
    for e in G.edges:
        if G.edges[e].get("subsurfaces").upper() == subsurface_name:
            return e
    raise Exception(f"No match for {subsurface_name} in {G.edges}")
        

# G, pos = create_base_graph(idf, path_to_input)
# G_afn = create_afn_graph(idf, G)
# f = draw_afn_over_init(G, G_afn, pos)


# medians = df.group_by(pl.col("space_names")).agg(pl.col("values").median())
# filtered_medians = medians.filter(pl.col("values") > 0)
# filtered_medians

# values = normalize_to_target(filtered_medians["values"], t_min=1, t_max=4)
# edges = [get_matching_edge(G, s) for s in filtered_medians["space_names"]]

# f = draw_afn_over_init(G, G_afn, pos)
# patches = nx.draw_networkx_edges(G, pos, edges, values)
# f.suptitle(curr_qoi)


# connectionstyle = [f"arc3,rad={r}" for r in accumulate([0.15] * 2)]
# nx.draw_networkx_nodes(Gm, pos)
# p = nx.draw_networkx_labels(Gm, pos)
# p = nx.draw_networkx_edges(Gm, pos, connectionstyle=connectionstyle)
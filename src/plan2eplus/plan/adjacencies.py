from itertools import combinations
from shapely import Polygon
import networkx as nx

# TODO check that have valid shape.. => maybe EP or geomeppy can help with this.. 



def check_adjacency(a: Polygon, b: Polygon):
    buffer_size=0.01
    return a.buffer(buffer_size).intersects(b.buffer(buffer_size, cap_style="square", join_style="bevel"))


def create_adjacencies(shapes: list[Polygon]):
    pairs = list(combinations(shapes, 2))
    print(pairs)
    for a, b in pairs:
        if check_adjacency(
            a, b
        ):
            print("found a match!")
            # G.add_edge(a, b)
            # G = generate_directed_adjacencies(
            #     G, domains[a], domains[b]
            # )


def generate_directed_adjacencies(G: Graph, domain_a: Domain, domain_b: Domain):
    cmp = domain_a.compare_domains(domain_b)
    for drn in [Direction.NORTH, Direction.EAST]:
        opp_drn = get_opposite_direction(drn)
        if cmp[drn.name]:
            d1, d2 = (
                (domain_a, domain_b)
                if cmp[drn.name] == domain_a
                else (domain_b, domain_a)
            )
            G.nodes[d1.name]["data"][opp_drn.name].append(d2.name)
            G.nodes[d2.name]["data"][drn.name].append(d1.name)

    return G
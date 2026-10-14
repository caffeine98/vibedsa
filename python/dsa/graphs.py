"""Two ways to store a graph: an adjacency list and an adjacency matrix."""

from collections.abc import Hashable, Iterable

Edge = tuple[Hashable, Hashable]


def adjacency_list(
    nodes: Iterable[Hashable], edges: Iterable[Edge], directed: bool = False
) -> dict[Hashable, list[Hashable]]:
    """Map each node to the list of nodes its edges lead to."""
    graph: dict[Hashable, list[Hashable]] = {node: [] for node in nodes}
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)  # an undirected edge goes both ways
    return graph


def adjacency_matrix(
    nodes: list[Hashable], edges: Iterable[Edge], directed: bool = False
) -> list[list[int]]:
    """matrix[i][j] is 1 if there is an edge from nodes[i] to nodes[j]."""
    index = {node: i for i, node in enumerate(nodes)}
    matrix = [[0] * len(nodes) for _ in nodes]
    for u, v in edges:
        matrix[index[u]][index[v]] = 1
        if not directed:
            matrix[index[v]][index[u]] = 1
    return matrix

"""Minimum spanning tree: Kruskal's and Prim's algorithms."""

import heapq
from collections.abc import Hashable

from dsa.union_find import UnionFind

Edge = tuple[Hashable, Hashable, float]  # (u, v, weight), undirected
MST = tuple[float, list[Edge]]  # (total weight, edges used)


def kruskal(nodes: list[Hashable], edges: list[Edge]) -> MST | None:
    """Add the cheapest edges first, skipping any that would form a cycle.

    Returns None if the graph isn't connected.
    """
    groups = UnionFind(nodes)
    total, used = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if groups.union(u, v):  # False means u and v were already joined
            total += w
            used.append((u, v, w))
    return (total, used) if len(used) == len(nodes) - 1 else None


def prim(nodes: list[Hashable], edges: list[Edge]) -> MST | None:
    """Grow one tree from the first node, always adding its cheapest edge.

    Returns None if the graph isn't connected.
    """
    if not nodes:
        return None
    graph: dict[Hashable, list] = {n: [] for n in nodes}  # (weight, next)
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))

    start = nodes[0]
    in_tree = {start}
    heap = [(w, start, v) for w, v in graph[start]]  # edges leaving the tree
    heapq.heapify(heap)
    total, used = 0, []
    while heap and len(in_tree) < len(nodes):
        w, u, v = heapq.heappop(heap)
        if v in in_tree:
            continue  # both ends are already in the tree
        in_tree.add(v)
        total += w
        used.append((u, v, w))
        for w2, nxt in graph[v]:
            if nxt not in in_tree:
                heapq.heappush(heap, (w2, v, nxt))
    return (total, used) if len(in_tree) == len(nodes) else None

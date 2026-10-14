"""Dijkstra's algorithm: shortest paths when edges have weights."""

import heapq
from collections.abc import Hashable

# node -> list of (neighbor, weight)
WeightedGraph = dict[Hashable, list[tuple[Hashable, float]]]


def dijkstra(
    graph: WeightedGraph, start: Hashable
) -> tuple[dict[Hashable, float], dict[Hashable, Hashable | None]]:
    """Return (dist, parent) for every node reachable from start."""
    if any(w < 0 for edges in graph.values() for _, w in edges):
        raise ValueError("Dijkstra's algorithm needs non-negative weights")

    dist = {start: 0}
    parent: dict[Hashable, Hashable | None] = {start: None}
    heap = [(0, start)]  # (distance so far, node), smallest first
    done = set()

    while heap:
        d, node = heapq.heappop(heap)
        if node in done:
            continue  # an old, longer entry for a node already settled
        done.add(node)  # d is now final: nothing can beat it
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_dist  # found a shorter way: relax
                parent[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))
    return dist, parent


def shortest_path(
    graph: WeightedGraph, start: Hashable, goal: Hashable
) -> tuple[float, list[Hashable]] | None:
    """(total weight, path) from start to goal, or None if unreachable."""
    dist, parent = dijkstra(graph, start)
    if goal not in dist:
        return None
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return dist[goal], path[::-1]

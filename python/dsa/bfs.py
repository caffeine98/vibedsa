"""Breadth-first search: visit nodes in order of distance from the start."""

from collections import deque
from collections.abc import Hashable

Graph = dict[Hashable, list[Hashable]]  # adjacency list


def bfs(graph: Graph, start: Hashable) -> dict[Hashable, Hashable | None]:
    """Return {node: parent} for every node reachable from start.

    Dict order is visit order. The start node's parent is None.
    """
    parent: dict[Hashable, Hashable | None] = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in parent:  # not seen yet
                parent[neighbor] = node  # mark it now, as it joins the queue
                queue.append(neighbor)
    return parent


def shortest_path(
    graph: Graph, start: Hashable, goal: Hashable
) -> list[Hashable] | None:
    """Fewest-edges path from start to goal, or None if there is none."""
    parent = bfs(graph, start)
    if goal not in parent:
        return None
    path = [goal]
    while path[-1] != start:  # follow parents back to the start
        path.append(parent[path[-1]])
    return path[::-1]


def distances(graph: Graph, start: Hashable) -> dict[Hashable, int]:
    """Number of edges from start to each reachable node."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

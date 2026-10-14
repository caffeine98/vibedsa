"""Topological sort with Kahn's algorithm."""

from collections import deque
from collections.abc import Hashable

Edge = tuple[Hashable, Hashable]  # (before, after)


def topological_sort(
    nodes: list[Hashable], edges: list[Edge]
) -> list[Hashable] | None:
    """Order nodes so every edge points forward. None if there's a cycle."""
    graph: dict[Hashable, list[Hashable]] = {node: [] for node in nodes}
    in_degree = {node: 0 for node in nodes}  # edges coming in
    for before, after in edges:
        graph[before].append(after)
        in_degree[after] += 1

    # Start with every node that has nothing before it.
    queue = deque(node for node in nodes if in_degree[node] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for after in graph[node]:
            in_degree[after] -= 1  # one fewer thing to wait for
            if in_degree[after] == 0:
                queue.append(after)

    # Nodes on a cycle never reach in-degree 0, so they're left out.
    return order if len(order) == len(nodes) else None

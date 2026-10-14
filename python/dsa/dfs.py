"""Depth-first search: follow one path as far as it goes, then back up."""

from collections.abc import Hashable

Graph = dict[Hashable, list[Hashable]]  # adjacency list


def dfs(graph: Graph, start: Hashable) -> list[Hashable]:
    """Nodes reachable from start, in the order DFS visits them."""
    visited: set[Hashable] = set()
    order: list[Hashable] = []

    def visit(node: Hashable) -> None:
        visited.add(node)
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visit(neighbor)  # go deeper before trying the next neighbor

    visit(start)
    return order


def dfs_iterative(graph: Graph, start: Hashable) -> list[Hashable]:
    """Same order as dfs(), using a stack instead of recursion."""
    visited: set[Hashable] = set()
    order: list[Hashable] = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:  # a node can be pushed more than once
            continue
        visited.add(node)
        order.append(node)
        # Push in reverse, so the first neighbor is popped first.
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)
    return order


def count_components(graph: Graph) -> int:
    """Number of separate pieces of an undirected graph."""
    visited: set[Hashable] = set()
    count = 0
    for node in graph:
        if node not in visited:
            count += 1  # a new piece: mark everything in it
            visited.update(dfs_iterative(graph, node))
    return count


def has_cycle(graph: Graph) -> bool:
    """True if a directed graph has a cycle."""
    # NEW: not visited yet. ACTIVE: on the current path. DONE: finished.
    NEW, ACTIVE, DONE = 0, 1, 2
    state = {node: NEW for node in graph}

    def visit(node: Hashable) -> bool:
        state[node] = ACTIVE
        for neighbor in graph[node]:
            if state[neighbor] == ACTIVE:
                return True  # an edge back into the current path
            if state[neighbor] == NEW and visit(neighbor):
                return True
        state[node] = DONE
        return False

    return any(state[node] == NEW and visit(node) for node in graph)

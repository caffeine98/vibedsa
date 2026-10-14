import graphlib
import random

from dsa.bfs import bfs, distances, shortest_path
from dsa.dfs import count_components, dfs, dfs_iterative, has_cycle
from dsa.graphs import adjacency_list, adjacency_matrix
from dsa.topological_sort import topological_sort

# The graphs drawn in the lessons.
NODES = list("ABCDEF")
EDGES = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("E", "F")]
TASKS = list("ABCDEF")
TASK_EDGES = [("A", "C"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("E", "F")]


def lesson_graph():
    return adjacency_list(NODES, EDGES)


def random_graph(rng, n, p, directed=False):
    nodes = list(range(n))
    edges = [
        (u, v)
        for u in nodes
        for v in nodes
        if u != v and (directed or u < v) and rng.random() < p
    ]
    return nodes, edges


# Representations


def test_adjacency_list_and_matrix():
    assert lesson_graph() == {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D", "E"],
        "D": ["B", "C"],
        "E": ["C", "F"],
        "F": ["E"],
    }
    m = adjacency_matrix(NODES, EDGES)
    assert m[0] == [0, 1, 1, 0, 0, 0]
    assert all(m[i][j] == m[j][i] for i in range(6) for j in range(6))


def test_directed_and_isolated_nodes():
    g = adjacency_list(["A", "B", "Z"], [("A", "B")], directed=True)
    assert g == {"A": ["B"], "B": [], "Z": []}


# BFS


def test_bfs_lesson_example():
    g = lesson_graph()
    assert list(bfs(g, "A")) == ["A", "B", "C", "D", "E", "F"]
    assert distances(g, "A") == {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2, "F": 3}
    assert shortest_path(g, "A", "F") == ["A", "C", "E", "F"]
    assert shortest_path(g, "A", "A") == ["A"]


def test_bfs_unreachable():
    g = adjacency_list(["A", "B", "C"], [("A", "B")])
    assert shortest_path(g, "A", "C") is None
    assert "C" not in distances(g, "A")


def brute_force_distances(graph, start):
    # Relax every edge until nothing changes. Slow, but obviously right.
    dist = {start: 0}
    changed = True
    while changed:
        changed = False
        for u in graph:
            for v in graph[u]:
                if u in dist and dist[u] + 1 < dist.get(v, float("inf")):
                    dist[v] = dist[u] + 1
                    changed = True
    return dist


def test_bfs_distances_match_brute_force():
    rng = random.Random(0)
    for _ in range(100):
        nodes, edges = random_graph(rng, rng.randint(1, 12), 0.25)
        g = adjacency_list(nodes, edges)
        assert distances(g, 0) == brute_force_distances(g, 0)
        for goal in nodes:
            path = shortest_path(g, 0, goal)
            if goal in distances(g, 0):
                assert len(path) - 1 == distances(g, 0)[goal]
                assert all(b in g[a] for a, b in zip(path, path[1:]))
            else:
                assert path is None


# DFS


def test_dfs_lesson_example():
    g = lesson_graph()
    assert dfs(g, "A") == ["A", "B", "D", "C", "E", "F"]
    assert dfs_iterative(g, "A") == ["A", "B", "D", "C", "E", "F"]


def test_dfs_versions_agree():
    rng = random.Random(0)
    for _ in range(200):
        nodes, edges = random_graph(rng, rng.randint(1, 12), 0.3)
        g = adjacency_list(nodes, edges)
        assert dfs(g, 0) == dfs_iterative(g, 0)
        assert set(dfs(g, 0)) == set(bfs(g, 0))  # same nodes reached


def test_components():
    g = adjacency_list(NODES + ["G", "H"], EDGES + [("G", "H")])
    assert count_components(g) == 2
    assert count_components(adjacency_list(["A", "B", "C"], [])) == 3
    assert count_components({}) == 0


def test_dfs_iterative_handles_long_paths():
    # 5,000 nodes in a line. Recursive DFS would hit the recursion limit.
    n = 5000
    g = adjacency_list(range(n), [(i, i + 1) for i in range(n - 1)])
    assert dfs_iterative(g, 0) == list(range(n))


# Cycles and topological sort


def test_topological_sort_lesson_example():
    assert topological_sort(TASKS, TASK_EDGES) == list("ABCDEF")
    assert topological_sort(TASKS, TASK_EDGES + [("F", "C")]) is None


def test_has_cycle_lesson_example():
    assert not has_cycle(adjacency_list(TASKS, TASK_EDGES, directed=True))
    cyclic = adjacency_list(TASKS, TASK_EDGES + [("F", "C")], directed=True)
    assert has_cycle(cyclic)


def test_cycle_edge_cases():
    assert has_cycle({"A": ["A"]})  # a self-loop is a cycle
    assert not has_cycle({})
    assert topological_sort([], []) == []
    assert topological_sort(["A"], [("A", "A")]) is None


def is_valid_order(order, nodes, edges):
    position = {node: i for i, node in enumerate(order)}
    return sorted(order) == sorted(nodes) and all(
        position[u] < position[v] for u, v in edges
    )


def test_topological_sort_and_cycles_match_graphlib():
    rng = random.Random(0)
    for _ in range(300):
        nodes, edges = random_graph(rng, rng.randint(1, 9), 0.15, directed=True)
        order = topological_sort(nodes, edges)

        sorter = graphlib.TopologicalSorter({n: [] for n in nodes})
        for u, v in edges:
            sorter.add(v, u)  # graphlib wants (node, *its predecessors)
        try:
            list(sorter.static_order())
            expected_cycle = False
        except graphlib.CycleError:
            expected_cycle = True

        assert (order is None) == expected_cycle
        assert has_cycle(adjacency_list(nodes, edges, directed=True)) == expected_cycle
        if order is not None:
            assert is_valid_order(order, nodes, edges)

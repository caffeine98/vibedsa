import itertools
import random

import pytest

from dsa.bfs import shortest_path as fewest_edges_path
from dsa.dijkstra import dijkstra, shortest_path
from dsa.mst import kruskal, prim
from dsa.union_find import UnionFind

# The weighted graph drawn in the lessons.
NODES = list("ABCDEF")
EDGES = [
    ("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8),
    ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "F", 3),
]  # fmt: skip


def weighted_graph(nodes, edges, directed=False):
    graph = {n: [] for n in nodes}
    for u, v, w in edges:
        graph[u].append((v, w))
        if not directed:
            graph[v].append((u, w))
    return graph


def random_edges(rng, n, p, max_weight=9):
    return [
        (u, v, rng.randint(0, max_weight))
        for u in range(n)
        for v in range(u + 1, n)
        if rng.random() < p
    ]


# Dijkstra


def test_dijkstra_lesson_example():
    g = weighted_graph(NODES, EDGES)
    dist, _ = dijkstra(g, "A")
    assert dist == {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13}
    assert shortest_path(g, "A", "F") == (13, ["A", "C", "B", "D", "E", "F"])


def test_fewest_edges_is_not_cheapest():
    # The lesson's point: BFS finds A-B-D-F (3 edges), which costs 15.
    g = weighted_graph(NODES, EDGES)
    unweighted = {n: [v for v, _ in g[n]] for n in NODES}
    path = fewest_edges_path(unweighted, "A", "F")
    assert path == ["A", "B", "D", "F"]
    weight = {(u, v): w for u, v, w in EDGES} | {(v, u): w for u, v, w in EDGES}
    assert sum(weight[a, b] for a, b in zip(path, path[1:])) == 15


def test_dijkstra_rejects_negative_weights():
    g = weighted_graph(["A", "B"], [("A", "B", -1)], directed=True)
    with pytest.raises(ValueError):
        dijkstra(g, "A")


def test_dijkstra_unreachable_and_start():
    g = weighted_graph(["A", "B", "C"], [("A", "B", 5)])
    assert shortest_path(g, "A", "C") is None
    assert shortest_path(g, "A", "A") == (0, ["A"])


def bellman_ford(graph, start):
    # Relax every edge V - 1 times. Slow, but a simple, trusted reference.
    dist = {start: 0}
    for _ in range(len(graph)):
        for u in graph:
            for v, w in graph[u]:
                if u in dist and dist[u] + w < dist.get(v, float("inf")):
                    dist[v] = dist[u] + w
    return dist


@pytest.mark.parametrize("directed", [False, True])
def test_dijkstra_matches_bellman_ford(directed):
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 10)
        edges = random_edges(rng, n, 0.35)
        if directed:  # randomly flip edge directions
            edges = [(v, u, w) if rng.random() < 0.5 else (u, v, w)
                     for u, v, w in edges]
        g = weighted_graph(range(n), edges, directed)
        dist, parent = dijkstra(g, 0)
        assert dist == bellman_ford(g, 0)
        for node in dist:  # every parent link is a real, tight edge
            if parent[node] is not None:
                p = parent[node]
                assert any(v == node and dist[p] + w == dist[node]
                           for v, w in g[p])


# Union-Find


def test_union_find_lesson_example():
    uf = UnionFind(NODES)
    for a, b in [("A", "B"), ("C", "D"), ("B", "D"), ("E", "F")]:
        assert uf.union(a, b)
    assert uf.parent == {"A": "A", "B": "A", "C": "A", "D": "C",
                         "E": "E", "F": "E"}
    assert uf.groups == 2
    assert uf.find("D") == "A"
    assert uf.parent["D"] == "A"  # path halving pointed D at its grandparent
    assert not uf.union("A", "D")  # already together


def test_union_find_matches_naive_labels():
    rng = random.Random(0)
    for _ in range(100):
        n = rng.randint(1, 20)
        uf = UnionFind(range(n))
        label = list(range(n))  # naive: relabel a whole group on each union
        for _ in range(rng.randint(0, 30)):
            a, b = rng.randrange(n), rng.randrange(n)
            merged = uf.union(a, b)
            assert merged == (label[a] != label[b])
            old, new = label[b], label[a]
            label = [new if x == old else x for x in label]
            for x in range(n):
                for y in range(n):
                    assert uf.connected(x, y) == (label[x] == label[y])
        assert uf.groups == len(set(label))


def test_union_by_size_keeps_trees_short():
    n = 1 << 12
    uf = UnionFind(range(n))
    for i in range(1, n):
        uf.union(0, i)  # without union by size, this could make a long chain
    depth = 0
    for x in range(n):
        d = 0
        while uf.parent[x] != x:
            x = uf.parent[x]
            d += 1
        depth = max(depth, d)
    assert depth <= 12  # at most log2(n)


# Minimum spanning tree


def test_mst_lesson_example():
    total, used = kruskal(NODES, EDGES)
    assert total == 13
    assert used == [("B", "C", 1), ("A", "C", 2), ("D", "E", 2),
                    ("E", "F", 3), ("B", "D", 5)]
    total, used = prim(NODES, EDGES)
    assert total == 13
    assert used == [("A", "C", 2), ("C", "B", 1), ("B", "D", 5),
                    ("D", "E", 2), ("E", "F", 3)]


def test_mst_is_not_shortest_paths():
    # The triangle from the lesson: the MST skips A-C, the shortest A-to-C route.
    edges = [("A", "B", 2), ("B", "C", 2), ("A", "C", 3)]
    total, used = kruskal(["A", "B", "C"], edges)
    assert total == 4 and ("A", "C", 3) not in used
    g = weighted_graph(["A", "B", "C"], edges)
    assert shortest_path(g, "A", "C") == (3, ["A", "C"])


def test_mst_disconnected_and_tiny():
    assert kruskal(["A", "B"], []) is None
    assert prim(["A", "B"], []) is None
    assert kruskal(["A"], []) == (0, [])
    assert prim(["A"], []) == (0, [])


def is_spanning_tree(n, used):
    uf = UnionFind(range(n))
    return len(used) == n - 1 and all(uf.union(u, v) for u, v, _ in used)


def brute_force_mst_total(n, edges):
    best = None
    for subset in itertools.combinations(edges, n - 1):
        if is_spanning_tree(n, subset):
            total = sum(w for _, _, w in subset)
            best = total if best is None else min(best, total)
    return best


def test_mst_matches_brute_force():
    rng = random.Random(0)
    for _ in range(150):
        n = rng.randint(1, 6)
        edges = random_edges(rng, n, 0.6)
        expected = brute_force_mst_total(n, edges)
        for algorithm in (kruskal, prim):
            result = algorithm(list(range(n)), edges)
            if expected is None:
                assert result is None
            else:
                total, used = result
                assert total == expected
                assert is_spanning_tree(n, used)

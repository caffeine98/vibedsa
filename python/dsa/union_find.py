"""Union-Find (disjoint set union): track which group each item is in."""

from collections.abc import Hashable, Iterable


class UnionFind:
    def __init__(self, items: Iterable[Hashable]) -> None:
        # Each item starts alone: its own parent, in a group of size 1.
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in self.parent}
        self.groups = len(self.parent)

    def find(self, x: Hashable) -> Hashable:
        """Return the root of x's group."""
        while self.parent[x] != x:
            # Path halving: point x at its grandparent as we climb.
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: Hashable, b: Hashable) -> bool:
        """Merge the groups of a and b. False if already together."""
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a  # make root_a the bigger group
        self.parent[root_b] = root_a  # hang the smaller tree under it
        self.size[root_a] += self.size[root_b]
        self.groups -= 1
        return True

    def connected(self, a: Hashable, b: Hashable) -> bool:
        return self.find(a) == self.find(b)

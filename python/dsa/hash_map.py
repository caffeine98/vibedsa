"""A hash map using separate chaining, and a hash set built on it.

Each bucket is a list of (key, value) pairs. Keys that land in the
same bucket (a collision) sit side by side in that list.
"""

from collections.abc import Hashable, Iterator
from typing import Any

Bucket = list[tuple[Hashable, Any]]
MAX_LOAD = 0.75  # grow when items per bucket goes above this


class HashMap:
    def __init__(self, num_buckets: int = 8) -> None:
        self.buckets: list[Bucket] = [[] for _ in range(num_buckets)]
        self.size = 0

    def _bucket(self, key: Hashable) -> Bucket:
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key: Hashable, value: Any) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # key exists: replace the value
                return
        bucket.append((key, value))
        self.size += 1
        if self.size > MAX_LOAD * len(self.buckets):
            self._resize(2 * len(self.buckets))

    def get(self, key: Hashable) -> Any:
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

    def contains(self, key: Hashable) -> bool:
        return any(k == key for k, _ in self._bucket(key))

    def remove(self, key: Hashable) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return
        raise KeyError(key)

    def _resize(self, num_buckets: int) -> None:
        old = self.buckets
        self.buckets = [[] for _ in range(num_buckets)]
        for bucket in old:
            for key, value in bucket:
                # The bucket count changed, so every key gets a new index.
                self._bucket(key).append((key, value))

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[Hashable]:
        for bucket in self.buckets:
            for key, _ in bucket:
                yield key


class HashSet:
    """A hash map that stores keys only."""

    def __init__(self) -> None:
        self.map = HashMap()

    def add(self, key: Hashable) -> None:
        self.map.put(key, True)

    def remove(self, key: Hashable) -> None:
        self.map.remove(key)

    def contains(self, key: Hashable) -> bool:
        return self.map.contains(key)

    def __len__(self) -> int:
        return len(self.map)

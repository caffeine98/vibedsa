import heapq
import random

import pytest

from dsa.bst import BST
from dsa.heap import MinHeap, heap_sort
from dsa.trees import (
    TreeNode,
    height,
    inorder,
    level_order,
    postorder,
    preorder,
)
from dsa.trie import Trie

LESSON_KEYS = [8, 3, 10, 1, 6, 14, 4, 7, 13]  # the tree drawn in the lessons


def lesson_tree():
    bst = BST()
    for k in LESSON_KEYS:
        bst.insert(k)
    return bst


def run(traversal, root):
    out = []
    traversal(root, out)
    return out


def iterative_height(node):
    # Recursion would hit Python's limit on the 1,000-level tree below.
    best, stack = 0, [(node, 1)] if node else []
    while stack:
        n, depth = stack.pop()
        best = max(best, depth)
        stack += [(c, depth + 1) for c in (n.left, n.right) if c]
    return best


# Trees and traversals


def test_traversals_of_lesson_tree():
    root = lesson_tree().root
    assert run(preorder, root) == [8, 3, 1, 6, 4, 7, 10, 14, 13]
    assert run(inorder, root) == [1, 3, 4, 6, 7, 8, 10, 13, 14]
    assert run(postorder, root) == [1, 4, 7, 6, 3, 13, 14, 10, 8]
    assert level_order(root) == [8, 3, 10, 1, 6, 14, 4, 7, 13]
    assert height(root) == 4


def test_traversals_of_empty_and_single():
    assert run(preorder, None) == []
    assert level_order(None) == []
    assert height(None) == 0
    one = TreeNode(5)
    assert run(inorder, one) == [5]
    assert height(one) == 1


# Binary search tree


def test_bst_insert_contains():
    bst = lesson_tree()
    assert len(bst) == 9
    assert all(bst.contains(k) for k in LESSON_KEYS)
    assert not bst.contains(5)
    assert not bst.insert(6)  # duplicate
    assert len(bst) == 9
    assert bst.min() == 1


def test_bst_delete_cases():
    bst = lesson_tree()
    assert bst.delete(13)  # leaf
    assert bst.delete(14)  # now a leaf
    assert bst.delete(3)  # two children: replaced by successor 4
    assert level_order(bst.root) == [8, 4, 10, 1, 6, 7]
    assert not bst.delete(99)
    assert list(bst) == [1, 4, 6, 7, 8, 10]


def test_bst_delete_example_from_lesson():
    bst = lesson_tree()
    bst.delete(3)
    assert level_order(bst.root) == [8, 4, 10, 1, 6, 14, 7, 13]


def test_bst_delete_root_until_empty():
    bst = lesson_tree()
    while bst.root is not None:
        bst.delete(bst.root.val)
    assert len(bst) == 0
    assert list(bst) == []
    with pytest.raises(ValueError):
        bst.min()


def test_bst_random_operations_match_set():
    rng = random.Random(0)
    bst, ref = BST(), set()
    for _ in range(3000):
        k = rng.randint(0, 200)
        if rng.random() < 0.6:
            assert bst.insert(k) == (k not in ref)
            ref.add(k)
        else:
            assert bst.delete(k) == (k in ref)
            ref.discard(k)
        assert len(bst) == len(ref)
    assert list(bst) == sorted(ref)


def test_bst_height_random_vs_sorted():
    # Numbers quoted in the lesson.
    shuffled = BST()
    for k in random.Random(1).sample(range(10_000), 1000):
        shuffled.insert(k)
    in_order = BST()
    for k in range(1000):
        in_order.insert(k)  # iterative insert: no recursion limit
    assert iterative_height(shuffled.root) == 22
    assert iterative_height(in_order.root) == 1000
    assert list(in_order) == list(range(1000))


# Heap


def test_heap_push_example_from_lesson():
    heap = MinHeap()
    for x in [5, 3, 8, 1, 4, 2]:
        heap.push(x)
    assert heap.items == [1, 3, 2, 5, 4, 8]
    assert heap.pop() == 1
    assert heap.items == [2, 3, 8, 5, 4]


def test_heap_property_holds():
    rng = random.Random(0)
    heap = MinHeap([rng.randint(0, 99) for _ in range(200)])
    a = heap.items
    for i in range(1, len(a)):
        assert a[(i - 1) // 2] <= a[i]


def test_heap_matches_heapq():
    rng = random.Random(0)
    heap, ref = MinHeap(), []
    for _ in range(3000):
        if rng.random() < 0.6 or not ref:
            x = rng.randint(-50, 50)
            heap.push(x)
            heapq.heappush(ref, x)
        else:
            assert heap.pop() == heapq.heappop(ref)
        assert len(heap) == len(ref)
        if ref:
            assert heap.peek() == ref[0]


def test_heap_build_then_drain_is_sorted():
    rng = random.Random(0)
    items = [rng.randint(0, 99) for _ in range(100)]
    heap = MinHeap(items)
    assert [heap.pop() for _ in range(100)] == sorted(items)


def test_empty_heap_errors():
    with pytest.raises(IndexError):
        MinHeap().pop()
    with pytest.raises(IndexError):
        MinHeap().peek()


@pytest.mark.parametrize(
    "items", [[], [1], [2, 1], [5, 3, 8, 1, 4, 2], [3, 3, 3], [5, 4, 3, 2, 1]]
)
def test_heap_sort_cases(items):
    copy = list(items)
    heap_sort(copy)
    assert copy == sorted(items)


def test_heap_sort_random():
    rng = random.Random(0)
    for _ in range(200):
        items = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        copy = list(items)
        heap_sort(copy)
        assert copy == sorted(items)


# Trie


def lesson_trie():
    trie = Trie()
    for w in ["car", "cart", "cat", "do", "dog"]:
        trie.insert(w)
    return trie


def test_trie_contains_vs_prefix():
    trie = lesson_trie()
    assert trie.contains("car")
    assert trie.contains("do")
    assert not trie.contains("ca")  # a prefix, not a word
    assert trie.starts_with("ca")
    assert not trie.starts_with("cb")
    assert not trie.contains("carts")


def test_trie_words_with_prefix():
    trie = lesson_trie()
    assert trie.words_with_prefix("ca") == ["car", "cart", "cat"]
    assert trie.words_with_prefix("do") == ["do", "dog"]
    assert trie.words_with_prefix("x") == []
    assert trie.words_with_prefix("") == ["car", "cart", "cat", "do", "dog"]


def test_trie_empty_word_and_repeats():
    trie = Trie()
    trie.insert("a")
    trie.insert("a")
    assert trie.words_with_prefix("") == ["a"]
    assert not trie.contains("")
    trie.insert("")
    assert trie.contains("")


def test_trie_random_words_match_reference():
    rng = random.Random(0)
    words = {"".join(rng.choice("abc") for _ in range(rng.randint(1, 5)))
             for _ in range(200)}
    trie = Trie()
    for w in words:
        trie.insert(w)
    for prefix in ["", "a", "ab", "abc", "c", "cc"]:
        expected = sorted(w for w in words if w.startswith(prefix))
        assert trie.words_with_prefix(prefix) == expected

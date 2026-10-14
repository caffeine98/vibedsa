"""A binary search tree of unique keys.

For every node: keys in its left subtree are smaller, and keys in its
right subtree are bigger.
"""

from typing import Any, Iterator

from dsa.trees import TreeNode


class BST:
    def __init__(self) -> None:
        self.root: TreeNode | None = None
        self.size = 0

    def contains(self, key: Any) -> bool:
        node = self.root
        while node is not None:
            if key == node.val:
                return True
            node = node.left if key < node.val else node.right
        return False

    def insert(self, key: Any) -> bool:
        """Add key. Return False if it was already there."""
        if self.root is None:
            self.root = TreeNode(key)
            self.size += 1
            return True
        node = self.root
        while True:
            if key == node.val:
                return False  # no duplicates
            if key < node.val:
                if node.left is None:
                    node.left = TreeNode(key)
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(key)
                    break
                node = node.right
        self.size += 1
        return True

    def delete(self, key: Any) -> bool:
        """Remove key. Return False if it wasn't there."""
        if not self.contains(key):
            return False
        self.root = _delete(self.root, key)
        self.size -= 1
        return True

    def min(self) -> Any:
        if self.root is None:
            raise ValueError("min of empty tree")
        node = self.root
        while node.left is not None:  # smallest key is furthest left
            node = node.left
        return node.val

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[Any]:
        """Keys in sorted order: an inorder walk, using a stack."""
        stack: list[TreeNode] = []
        node = self.root
        while stack or node is not None:
            while node is not None:  # go as far left as possible
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.val
            node = node.right


def _delete(node: TreeNode | None, key: Any) -> TreeNode | None:
    """Delete key from this subtree. Return the subtree's new root."""
    if node is None:
        return None
    if key < node.val:
        node.left = _delete(node.left, key)
    elif key > node.val:
        node.right = _delete(node.right, key)
    else:
        if node.left is None:  # 0 or 1 child: the child takes its place
            return node.right
        if node.right is None:
            return node.left
        # 2 children: copy in the next bigger key, then delete that one.
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.val = successor.val
        node.right = _delete(node.right, successor.val)
    return node

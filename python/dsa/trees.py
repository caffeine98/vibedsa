"""A binary tree node, and the four ways to visit every node."""

from collections import deque
from typing import Any


class TreeNode:
    def __init__(
        self,
        val: Any,
        left: "TreeNode | None" = None,
        right: "TreeNode | None" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def preorder(node: TreeNode | None, out: list[Any]) -> None:
    """Node, then left subtree, then right subtree."""
    if node is None:
        return
    out.append(node.val)
    preorder(node.left, out)
    preorder(node.right, out)


def inorder(node: TreeNode | None, out: list[Any]) -> None:
    """Left subtree, then node, then right subtree."""
    if node is None:
        return
    inorder(node.left, out)
    out.append(node.val)
    inorder(node.right, out)


def postorder(node: TreeNode | None, out: list[Any]) -> None:
    """Left subtree, then right subtree, then node."""
    if node is None:
        return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)


def level_order(root: TreeNode | None) -> list[Any]:
    """Level by level, left to right. Uses a queue, not recursion."""
    out = []
    queue = deque([root] if root else [])
    while queue:
        node = queue.popleft()
        out.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return out


def height(node: TreeNode | None) -> int:
    """Number of levels. An empty tree has height 0."""
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))

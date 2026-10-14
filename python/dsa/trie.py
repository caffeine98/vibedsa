"""A trie (prefix tree) of words. Each edge is one letter."""


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False  # does a word end here?


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

    def _find(self, prefix: str) -> TrieNode | None:
        """Follow prefix letter by letter. None if the path breaks off."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def contains(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def words_with_prefix(self, prefix: str) -> list[str]:
        """Every stored word that starts with prefix, in sorted order."""
        node = self._find(prefix)
        words: list[str] = []
        if node is not None:
            _collect(node, prefix, words)
        return words


def _collect(node: TrieNode, path: str, words: list[str]) -> None:
    """Add every word in this subtree to words. path spells node's letters."""
    if node.is_word:
        words.append(path)
    for ch in sorted(node.children):
        _collect(node.children[ch], path + ch, words)

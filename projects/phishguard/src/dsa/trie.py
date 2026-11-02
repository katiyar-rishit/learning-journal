"""
PhishGuard - Custom Trie (Prefix Tree) for Suspicious Phrase Detection
Academic Data Structures & Algorithms Implementation

Implements a Trie supporting single and multiword phrase detection,
prefix searches, word boundary enforcement (to prevent false substring matches),
and structural tree exports for classroom visualization.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple


class TrieNode:
    """A single node within the prefix Trie."""

    def __init__(self, char: str = ""):
        self.char: str = char
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_phrase: bool = False
        self.full_phrase: Optional[str] = None
        self.metadata: Optional[Dict[str, Any]] = None

    def __repr__(self) -> str:
        return f"TrieNode(char={self.char!r}, is_end={self.is_end_of_phrase}, phrase={self.full_phrase!r})"


class SuspiciousPhraseTrie:
    """
    Custom Trie for storing and rapidly matching suspicious terms & multiword phrases.
    
    Time Complexity:
    - Insert: O(L), where L is phrase length
    - Search Exact: O(L)
    - Prefix Search: O(P), where P is prefix length
    - Delete: O(L)
    - Text Scanning: O(N * L_max), where N is text length and L_max is max phrase length.
    
    Space Complexity:
    - O(Sigma * L * W), where Sigma is alphabet size, L is average phrase length, W is number of phrases.
    """

    def __init__(self):
        self.root: TrieNode = TrieNode("")
        self._phrase_count: int = 0

    @property
    def size(self) -> int:
        return self._phrase_count

    def insert(self, phrase: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Insert a word or multiword phrase into the Trie.
        Stored in lowercase for case-insensitive matching.
        """
        if not phrase or not phrase.strip():
            return

        normalized = phrase.strip().lower()
        curr = self.root

        for char in normalized:
            if char not in curr.children:
                curr.children[char] = TrieNode(char)
            curr = curr.children[char]

        if not curr.is_end_of_phrase:
            self._phrase_count += 1

        curr.is_end_of_phrase = True
        curr.full_phrase = normalized
        curr.metadata = metadata or {}

    def search_exact(self, phrase: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Exact search for a word or multiword phrase.
        Returns (is_found, metadata).
        """
        if not phrase:
            return False, None

        normalized = phrase.strip().lower()
        curr = self.root

        for char in normalized:
            if char not in curr.children:
                return False, None
            curr = curr.children[char]

        if curr.is_end_of_phrase:
            return True, curr.metadata
        return False, None

    def starts_with(self, prefix: str) -> bool:
        """Check if any phrase in the Trie starts with the given prefix."""
        if not prefix:
            return True

        normalized = prefix.strip().lower()
        curr = self.root

        for char in normalized:
            if char not in curr.children:
                return False
            curr = curr.children[char]

        return True

    def get_words_with_prefix(self, prefix: str, limit: int = 50) -> List[str]:
        """
        Returns all phrases stored in the Trie that begin with prefix.
        Uses recursive Depth-First Search (DFS).
        """
        normalized = prefix.strip().lower()
        curr = self.root

        for char in normalized:
            if char not in curr.children:
                return []
            curr = curr.children[char]

        results: List[str] = []

        def _dfs(node: TrieNode) -> None:
            if len(results) >= limit:
                return
            if node.is_end_of_phrase and node.full_phrase:
                results.append(node.full_phrase)
            for child in node.children.values():
                _dfs(child)

        _dfs(curr)
        return results

    def delete(self, phrase: str) -> bool:
        """
        Delete a phrase from the Trie if present.
        Recursively prunes childless non-terminal nodes.
        Returns True if phrase was found and deleted, False otherwise.
        """
        if not phrase:
            return False

        normalized = phrase.strip().lower()
        found_and_deleted = False

        def _delete_helper(node: TrieNode, text: str, index: int) -> bool:
            nonlocal found_and_deleted

            if index == len(text):
                if not node.is_end_of_phrase:
                    return False  # Phrase not marked as end of word
                node.is_end_of_phrase = False
                node.full_phrase = None
                node.metadata = None
                self._phrase_count -= 1
                found_and_deleted = True
                # Return True if this node can be pruned from parent
                return len(node.children) == 0

            char = text[index]
            if char not in node.children:
                return False

            can_prune_child = _delete_helper(node.children[char], text, index + 1)

            if can_prune_child:
                del node.children[char]

            # Current node can be pruned if it is not end-of-phrase and has no remaining children
            return (not node.is_end_of_phrase) and (len(node.children) == 0)

        _delete_helper(self.root, normalized, 0)
        return found_and_deleted

    def match_in_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Scans email text and identifies all registered suspicious phrases.
        
        CRITICAL DSA FEATURE - Word Boundary Enforcement:
        - Only initiates matching at a word boundary (prevents matching 'urgent' inside 'detergent').
        - Only accepts an end-of-phrase match if it terminates at a word boundary.
        - Returns list of matched indicators with start/end character offsets for highlighting.
        """
        if not text:
            return []

        text_lower = text.lower()
        text_len = len(text_lower)
        matches: List[Dict[str, Any]] = []
        matched_spans: List[Tuple[int, int]] = []

        def _is_word_boundary(pos: int, is_start: bool) -> bool:
            if is_start:
                return pos == 0 or not text_lower[pos - 1].isalnum()
            else:
                return pos >= text_len - 1 or not text_lower[pos + 1].isalnum()

        for start_idx in range(text_len):
            # Enforce start word boundary
            if not _is_word_boundary(start_idx, is_start=True):
                continue

            curr = self.root
            deepest_match: Optional[Dict[str, Any]] = None

            for curr_idx in range(start_idx, text_len):
                char = text_lower[curr_idx]
                if char not in curr.children:
                    break
                curr = curr.children[char]

                if curr.is_end_of_phrase:
                    # Enforce end word boundary
                    if _is_word_boundary(curr_idx, is_start=False):
                        deepest_match = {
                            "term": curr.full_phrase,
                            "original_text": text[start_idx : curr_idx + 1],
                            "start_pos": start_idx,
                            "end_pos": curr_idx + 1,
                            "metadata": curr.metadata or {},
                        }

            if deepest_match:
                # Avoid overlapping duplicate spans (prefer longer phrase)
                is_subspan = False
                for m_start, m_end in matched_spans:
                    if (deepest_match["start_pos"] >= m_start and deepest_match["end_pos"] <= m_end):
                        is_subspan = True
                        break

                if not is_subspan:
                    matches.append(deepest_match)
                    matched_spans.append((deepest_match["start_pos"], deepest_match["end_pos"]))

        return matches

    def get_structure_stats(self) -> Dict[str, Any]:
        """Returns structural statistics about the Trie for display."""
        total_nodes = 0
        max_depth = 0
        terminal_nodes = 0

        def _dfs(node: TrieNode, depth: int):
            nonlocal total_nodes, max_depth, terminal_nodes
            total_nodes += 1
            if depth > max_depth:
                max_depth = depth
            if node.is_end_of_phrase:
                terminal_nodes += 1
            for child in node.children.values():
                _dfs(child, depth + 1)

        _dfs(self.root, 0)

        return {
            "total_nodes": total_nodes,
            "stored_phrases": self._phrase_count,
            "max_depth": max_depth,
            "terminal_nodes": terminal_nodes,
            "root_branches": len(self.root.children),
        }

    def get_graph_edges(self, max_nodes: int = 80) -> List[Dict[str, str]]:
        """
        Exports a trimmed list of edges (parent -> child) for visualization in Plotly or Graphviz.
        """
        edges: List[Dict[str, str]] = []
        node_counter = 0

        def _traverse(node: TrieNode, parent_label: str):
            nonlocal node_counter
            if node_counter >= max_nodes:
                return

            for char, child in sorted(node.children.items()):
                node_counter += 1
                child_label = f"Node_{node_counter} ('{char}')"
                if child.is_end_of_phrase:
                    child_label += f" [END: {child.full_phrase}]"

                edges.append({
                    "from": parent_label,
                    "to": child_label,
                    "char": char,
                    "is_end": str(child.is_end_of_phrase),
                })
                _traverse(child, child_label)

        _traverse(self.root, "Root")
        return edges

"""
Core custom Data Structures and Algorithms package for PhishGuard.
Academic implementations with separate chaining, linked nodes, and recursive sorting.
"""

from .hash_table import SeparateChainingHashTable
from .trie import SuspiciousPhraseTrie, TrieNode
from .queue import LinkedQueue, QueueNode
from .linked_list import SinglyLinkedList, AnalysisNode
from .merge_sort import merge_sort_analyses, merge_sort_with_trace
from .binary_search import binary_search_by_id, binary_search_with_trace

__all__ = [
    "SeparateChainingHashTable",
    "SuspiciousPhraseTrie",
    "TrieNode",
    "LinkedQueue",
    "QueueNode",
    "SinglyLinkedList",
    "AnalysisNode",
    "merge_sort_analyses",
    "merge_sort_with_trace",
    "binary_search_by_id",
    "binary_search_with_trace",
]

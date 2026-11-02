"""
PhishGuard - Custom Separate Chaining Hash Table
Academic Data Structures & Algorithms Implementation

Implements a hash table using separate chaining for collision handling,
complete with linked HashEntry nodes, dynamic table resizing, and
inspection utilities for classroom demonstration and Streamlit visualization.
"""

from typing import Any, Dict, List, Optional, Tuple


class HashEntry:
    """Linked list node used in each hash table bucket for separate chaining."""

    def __init__(self, key: str, value: Any, next_node: Optional["HashEntry"] = None):
        self.key: str = key
        self.value: Any = value
        self.next: Optional["HashEntry"] = next_node

    def __repr__(self) -> str:
        return f"HashEntry(key={self.key!r}, value={self.value!r})"


class SeparateChainingHashTable:
    """
    Hash Table with Separate Chaining for collision resolution.
    
    Time Complexity:
    - Average Case: Insert O(1), Search O(1), Delete O(1)
    - Worst Case: Insert O(n), Search O(n), Delete O(n) (when all keys collide into one bucket)
    
    Space Complexity:
    - O(m + n), where m = capacity (number of buckets) and n = total entries stored.
    """

    def __init__(self, initial_capacity: int = 16, load_factor_threshold: float = 0.75):
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be greater than 0.")
        if load_factor_threshold <= 0:
            raise ValueError("Load factor threshold must be greater than 0.")

        self._capacity: int = initial_capacity
        self._load_factor_threshold: float = load_factor_threshold
        self._size: int = 0
        self._buckets: List[Optional[HashEntry]] = [None] * self._capacity

    def _hash(self, key: str) -> int:
        """
        Polynomial rolling hash function for strings.
        hash(s) = sum(s[i] * p^i) % capacity, where p = 31.
        Deterministic, robust, and educational.
        """
        p = 31
        hash_val = 0
        p_pow = 1
        for char in key:
            hash_val = (hash_val + ord(char) * p_pow)
            p_pow = (p_pow * p)
        return hash_val % self._capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def size(self) -> int:
        return self._size

    @property
    def load_factor(self) -> float:
        return self._size / self._capacity if self._capacity > 0 else 0.0

    def insert(self, key: str, value: Any) -> bool:
        """
        Insert or update a key-value pair.
        Returns True if a new key was inserted, False if an existing key was updated.
        """
        if not isinstance(key, str):
            key = str(key)

        index = self._hash(key)
        curr = self._buckets[index]

        # Check if key already exists in the chain; if so, update its value
        while curr is not None:
            if curr.key == key:
                curr.value = value
                return False
            curr = curr.next

        # Key does not exist; prepend new node to the bucket's linked chain
        new_entry = HashEntry(key=key, value=value, next_node=self._buckets[index])
        self._buckets[index] = new_entry
        self._size += 1

        # Check load factor and resize if needed
        if self.load_factor >= self._load_factor_threshold:
            self._resize(self._capacity * 2)

        return True

    def search(self, key: str) -> Optional[Any]:
        """
        Search for a key and return its associated value, or None if not found.
        """
        if not isinstance(key, str):
            key = str(key)

        index = self._hash(key)
        curr = self._buckets[index]

        while curr is not None:
            if curr.key == key:
                return curr.value
            curr = curr.next

        return None

    def get(self, key: str, default: Any = None) -> Any:
        """Search with a fallback default value."""
        val = self.search(key)
        return default if val is None else val

    def update(self, key: str, value: Any) -> bool:
        """
        Update the value of an existing key.
        Returns True if key was found and updated, False otherwise.
        """
        if not isinstance(key, str):
            key = str(key)

        index = self._hash(key)
        curr = self._buckets[index]

        while curr is not None:
            if curr.key == key:
                curr.value = value
                return True
            curr = curr.next

        return False

    def delete(self, key: str) -> bool:
        """
        Delete a key from the hash table.
        Returns True if deleted, False if key was not found.
        """
        if not isinstance(key, str):
            key = str(key)

        index = self._hash(key)
        curr = self._buckets[index]
        prev: Optional[HashEntry] = None

        while curr is not None:
            if curr.key == key:
                if prev is None:
                    # Deleting the head node of this bucket
                    self._buckets[index] = curr.next
                else:
                    # Deleting an internal or tail node
                    prev.next = curr.next

                self._size -= 1
                return True

            prev = curr
            curr = curr.next

        return False

    def contains(self, key: str) -> bool:
        """Check whether key exists in the hash table."""
        return self.search(key) is not None

    def _resize(self, new_capacity: int) -> None:
        """
        Resize bucket array and rehash all active entries.
        Preserves all existing key-value pairs in new bucket indices.
        """
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0  # Re-incremented during insertion

        for head in old_buckets:
            curr = head
            while curr is not None:
                self.insert(curr.key, curr.value)
                curr = curr.next

    def get_collision_stats(self) -> Dict[str, Any]:
        """
        Compute diagnostic metrics for classroom demonstration:
        - Capacity, Size, Load Factor
        - Non-empty buckets count
        - Collisions (entries sharing a bucket beyond the 1st entry)
        - Max chain length
        - Average chain length (for non-empty buckets)
        """
        non_empty = 0
        max_chain = 0
        total_chain_lengths = 0
        collisions = 0

        for head in self._buckets:
            chain_len = 0
            curr = head
            while curr is not None:
                chain_len += 1
                curr = curr.next

            if chain_len > 0:
                non_empty += 1
                total_chain_lengths += chain_len
                if chain_len > 1:
                    collisions += (chain_len - 1)
                if chain_len > max_chain:
                    max_chain = chain_len

        avg_chain = (total_chain_lengths / non_empty) if non_empty > 0 else 0.0

        return {
            "capacity": self._capacity,
            "size": self._size,
            "load_factor": round(self.load_factor, 4),
            "non_empty_buckets": non_empty,
            "empty_buckets": self._capacity - non_empty,
            "total_collisions": collisions,
            "max_chain_length": max_chain,
            "avg_chain_length": round(avg_chain, 2),
        }

    def get_buckets_view(self) -> List[Dict[str, Any]]:
        """
        Returns structured view of all buckets and their chains
        for UI display and interactive visualization.
        """
        view = []
        for idx, head in enumerate(self._buckets):
            chain = []
            curr = head
            while curr is not None:
                chain.append({
                    "key": curr.key,
                    "value": curr.value
                })
                curr = curr.next

            view.append({
                "bucket_index": idx,
                "chain_length": len(chain),
                "entries": chain
            })
        return view

    def keys(self) -> List[str]:
        """Return list of all keys in the hash table."""
        res = []
        for head in self._buckets:
            curr = head
            while curr is not None:
                res.append(curr.key)
                curr = curr.next
        return res

    def values(self) -> List[Any]:
        """Return list of all values in the hash table."""
        res = []
        for head in self._buckets:
            curr = head
            while curr is not None:
                res.append(curr.value)
                curr = curr.next
        return res

    def items(self) -> List[Tuple[str, Any]]:
        """Return list of (key, value) pairs."""
        res = []
        for head in self._buckets:
            curr = head
            while curr is not None:
                res.append((curr.key, curr.value))
                curr = curr.next
        return res

    def clear(self) -> None:
        """Reset the hash table to an empty state."""
        self._buckets = [None] * self._capacity
        self._size = 0

    # Magic methods for Pythonic dict-like syntax
    def __getitem__(self, key: str) -> Any:
        val = self.search(key)
        if val is None:
            raise KeyError(f"Key {key!r} not found in hash table.")
        return val

    def __setitem__(self, key: str, value: Any) -> None:
        self.insert(key, value)

    def __delitem__(self, key: str) -> None:
        deleted = self.delete(key)
        if not deleted:
            raise KeyError(f"Key {key!r} not found in hash table.")

    def __contains__(self, key: str) -> bool:
        return self.contains(key)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"SeparateChainingHashTable(size={self._size}, capacity={self._capacity}, load_factor={self.load_factor:.2f})"

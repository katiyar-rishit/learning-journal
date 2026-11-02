"""
Unit tests for SeparateChainingHashTable.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dsa.hash_table import SeparateChainingHashTable


def test_insert_and_search():
    ht = SeparateChainingHashTable(initial_capacity=4)
    assert ht.size == 0
    assert ht.is_empty if hasattr(ht, 'is_empty') else len(ht) == 0

    assert ht.insert("urgent", {"weight": 2.5, "category": "URGENCY"}) is True
    assert ht.size == 1

    val = ht.search("urgent")
    assert val is not None
    assert val["weight"] == 2.5
    assert val["category"] == "URGENCY"


def test_update_existing_key():
    ht = SeparateChainingHashTable(initial_capacity=8)
    ht.insert("urgent", 1.0)
    assert ht.search("urgent") == 1.0

    # Updating via insert should return False (key already existed)
    assert ht.insert("urgent", 2.5) is False
    assert ht.size == 1
    assert ht.search("urgent") == 2.5

    # Updating via explicit update
    assert ht.update("urgent", 3.0) is True
    assert ht.search("urgent") == 3.0
    assert ht.update("non_existent", 1.0) is False


def test_delete():
    ht = SeparateChainingHashTable(initial_capacity=8)
    ht.insert("a", 10)
    ht.insert("b", 20)
    ht.insert("c", 30)
    assert ht.size == 3

    assert ht.delete("b") is True
    assert ht.size == 2
    assert ht.search("b") is None
    assert ht.search("a") == 10
    assert ht.search("c") == 30

    # Delete non-existent key
    assert ht.delete("non_existent") is False
    assert ht.size == 2


def test_collision_handling():
    # Force small capacity to guarantee collisions
    ht = SeparateChainingHashTable(initial_capacity=2, load_factor_threshold=10.0)
    keys = ["apple", "banana", "cherry", "date", "fig", "grape"]
    for k in keys:
        ht.insert(k, len(k))

    assert ht.size == len(keys)
    # Check that all keys are retrievable despite collisions
    for k in keys:
        assert ht.search(k) == len(k)

    stats = ht.get_collision_stats()
    assert stats["total_collisions"] > 0
    assert stats["max_chain_length"] >= 2


def test_table_resizing():
    initial_cap = 4
    ht = SeparateChainingHashTable(initial_capacity=initial_cap, load_factor_threshold=0.75)
    # Adding 4 items should trigger resize
    for i in range(5):
        ht.insert(f"key_{i}", i * 10)

    assert ht.capacity > initial_cap
    assert ht.size == 5
    for i in range(5):
        assert ht.search(f"key_{i}") == i * 10


def test_magic_methods():
    ht = SeparateChainingHashTable()
    ht["password"] = 4.0
    assert "password" in ht
    assert ht["password"] == 4.0
    assert len(ht) == 1

    del ht["password"]
    assert "password" not in ht
    with pytest.raises(KeyError):
        _ = ht["password"]

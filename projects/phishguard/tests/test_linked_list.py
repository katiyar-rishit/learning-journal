"""
Unit tests for custom SinglyLinkedList and AnalysisNode.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dsa.linked_list import SinglyLinkedList, AnalysisNode


def _make_node(node_id: str, risk: float, label: int) -> AnalysisNode:
    return AnalysisNode(
        analysis_id=node_id,
        email_text=f"Sample text for {node_id}",
        predicted_class=label,
        ml_probability=risk,
        rule_score=risk * 10,
        final_risk_score=risk,
        risk_category="High" if risk > 0.5 else "Low",
    )


def test_linked_list_append_and_traverse():
    ll = SinglyLinkedList()
    assert ll.is_empty() is True
    assert ll.size == 0

    n1 = _make_node("ID-1", 0.9, 1)
    n2 = _make_node("ID-2", 0.1, 0)
    n3 = _make_node("ID-3", 0.6, 1)

    ll.append(n1)
    ll.append(n2)
    ll.append(n3)

    assert ll.size == 3
    assert ll.is_empty() is False

    records = ll.to_list()
    assert len(records) == 3
    assert records[0]["analysis_id"] == "ID-1"
    assert records[1]["analysis_id"] == "ID-2"
    assert records[2]["analysis_id"] == "ID-3"


def test_search_by_id():
    ll = SinglyLinkedList()
    n1 = _make_node("ID-1", 0.9, 1)
    n2 = _make_node("ID-2", 0.1, 0)
    ll.append(n1)
    ll.append(n2)

    found = ll.search_by_id("ID-2")
    assert found is not None
    assert found.analysis_id == "ID-2"
    assert found.predicted_class == 0

    not_found = ll.search_by_id("ID-999")
    assert not_found is None


def test_delete_by_id():
    ll = SinglyLinkedList()
    n1 = _make_node("ID-1", 0.9, 1)
    n2 = _make_node("ID-2", 0.1, 0)
    n3 = _make_node("ID-3", 0.6, 1)
    ll.append(n1)
    ll.append(n2)
    ll.append(n3)

    # Delete middle node
    assert ll.delete_by_id("ID-2") is True
    assert ll.size == 2
    assert ll.search_by_id("ID-2") is None
    assert ll.search_by_id("ID-1") is not None
    assert ll.search_by_id("ID-3") is not None

    # Delete head node
    assert ll.delete_by_id("ID-1") is True
    assert ll.size == 1
    assert ll.search_by_id("ID-1") is None
    assert ll.search_by_id("ID-3") is not None

    # Delete tail node
    assert ll.delete_by_id("ID-3") is True
    assert ll.size == 0
    assert ll.is_empty() is True

    # Delete from empty
    assert ll.delete_by_id("ID-999") is False


def test_clear():
    ll = SinglyLinkedList()
    ll.append(_make_node("ID-1", 0.9, 1))
    ll.append(_make_node("ID-2", 0.2, 0))
    assert ll.size == 2

    ll.clear()
    assert ll.size == 0
    assert ll.is_empty() is True
    assert ll.to_list() == []

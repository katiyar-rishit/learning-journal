"""
Unit tests for custom Binary Search and indexed array utilities.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dsa.binary_search import (
    binary_search_by_id,
    binary_search_with_trace,
    prepare_sorted_index_by_id,
)


def test_binary_search_found():
    records = [
        {"analysis_id": "PHISH-001", "risk": 0.9},
        {"analysis_id": "PHISH-002", "risk": 0.2},
        {"analysis_id": "PHISH-003", "risk": 0.7},
        {"analysis_id": "PHISH-004", "risk": 0.4},
    ]
    sorted_idx = prepare_sorted_index_by_id(records)

    found = binary_search_by_id(sorted_idx, "PHISH-003")
    assert found is not None
    assert found["analysis_id"] == "PHISH-003"
    assert found["risk"] == 0.7


def test_binary_search_not_found():
    records = [
        {"analysis_id": "PHISH-001", "risk": 0.9},
        {"analysis_id": "PHISH-002", "risk": 0.2},
    ]
    sorted_idx = prepare_sorted_index_by_id(records)

    found = binary_search_by_id(sorted_idx, "PHISH-999")
    assert found is None


def test_binary_search_trace():
    records = [
        {"analysis_id": "ID_01"},
        {"analysis_id": "ID_02"},
        {"analysis_id": "ID_03"},
        {"analysis_id": "ID_04"},
        {"analysis_id": "ID_05"},
    ]
    found, trace = binary_search_with_trace(records, "ID_04")
    assert found is not None
    assert found["analysis_id"] == "ID_04"
    assert len(trace) >= 1
    assert any("MATCH FOUND" in t["decision"] for t in trace)

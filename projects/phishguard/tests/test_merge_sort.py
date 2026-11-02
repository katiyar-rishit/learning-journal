"""
Unit tests for custom Merge Sort implementation and trace logging.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dsa.merge_sort import merge_sort_analyses, merge_sort_with_trace


def test_merge_sort_descending():
    records = [
        {"analysis_id": "A1", "final_risk_score": 0.25},
        {"analysis_id": "A2", "final_risk_score": 0.95},
        {"analysis_id": "A3", "final_risk_score": 0.50},
        {"analysis_id": "A4", "final_risk_score": 0.10},
        {"analysis_id": "A5", "final_risk_score": 0.75},
    ]

    sorted_records = merge_sort_analyses(records, descending=True)
    scores = [r["final_risk_score"] for r in sorted_records]
    assert scores == [0.95, 0.75, 0.50, 0.25, 0.10]
    assert sorted_records[0]["analysis_id"] == "A2"
    assert sorted_records[-1]["analysis_id"] == "A4"


def test_merge_sort_deterministic_ties():
    """
    CRITICAL TEST: Ensure tie scores are handled deterministically using analysis_id.
    """
    records = [
        {"analysis_id": "ID_B", "final_risk_score": 0.80},
        {"analysis_id": "ID_A", "final_risk_score": 0.80},
        {"analysis_id": "ID_C", "final_risk_score": 0.80},
    ]

    sorted_records = merge_sort_analyses(records, descending=True)
    ids = [r["analysis_id"] for r in sorted_records]
    # For descending, ID_C > ID_B > ID_A
    assert ids == ["ID_C", "ID_B", "ID_A"]


def test_merge_sort_edge_cases():
    assert merge_sort_analyses([]) == []
    single = [{"analysis_id": "ID_1", "final_risk_score": 0.5}]
    assert merge_sort_analyses(single) == single


def test_merge_sort_with_trace():
    records = [
        {"analysis_id": "A1", "final_risk_score": 0.3},
        {"analysis_id": "A2", "final_risk_score": 0.8},
        {"analysis_id": "A3", "final_risk_score": 0.1},
        {"analysis_id": "A4", "final_risk_score": 0.9},
    ]

    sorted_res, trace = merge_sort_with_trace(records, descending=True)
    assert len(sorted_res) == 4
    assert [r["final_risk_score"] for r in sorted_res] == [0.9, 0.8, 0.3, 0.1]
    assert len(trace) > 0

    types = [t["type"] for t in trace]
    assert "DIVIDE" in types
    assert "MERGE" in types

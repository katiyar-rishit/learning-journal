"""
PhishGuard - Custom Merge Sort for Risk Ranking
Academic Data Structures & Algorithms Implementation

Implements a pure recursive Merge Sort algorithm for sorting analysis records
in descending order of risk score, complete with deterministic tie-breaking,
trace instrumentation for classroom visualization, and divide-and-conquer tracking.
"""

from typing import Any, Dict, List, Optional, Tuple


def _compare_records(a: Dict[str, Any], b: Dict[str, Any], descending: bool = True) -> bool:
    """
    Compares two analysis records with deterministic tie-breaking.
    Primary key: final_risk_score
    Secondary key: analysis_id (lexicographic)
    
    Returns True if record 'a' should come BEFORE record 'b'.
    """
    score_a = a.get("final_risk_score", 0.0)
    score_b = b.get("final_risk_score", 0.0)

    if score_a != score_b:
        if descending:
            return score_a > score_b
        else:
            return score_a < score_b

    # Deterministic tie-breaker: compare analysis_id
    id_a = str(a.get("analysis_id", ""))
    id_b = str(b.get("analysis_id", ""))
    return id_a > id_b if descending else id_a < id_b


def merge_sort_analyses(
    records: List[Dict[str, Any]],
    descending: bool = True
) -> List[Dict[str, Any]]:
    """
    Standard recursive Merge Sort without trace logging.
    Time Complexity: O(n log n) in all cases (best, average, worst).
    Space Complexity: O(n) auxiliary space for sub-arrays.
    """
    if len(records) <= 1:
        return list(records)

    mid = len(records) // 2
    left = merge_sort_analyses(records[:mid], descending=descending)
    right = merge_sort_analyses(records[mid:], descending=descending)

    return _merge(left, right, descending=descending)


def _merge(
    left: List[Dict[str, Any]],
    right: List[Dict[str, Any]],
    descending: bool = True
) -> List[Dict[str, Any]]:
    """Merges two sorted lists into a single sorted list."""
    merged: List[Dict[str, Any]] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if _compare_records(left[i], right[j], descending=descending):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def merge_sort_with_trace(
    records: List[Dict[str, Any]],
    descending: bool = True
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Educational Merge Sort that logs every divide and merge operation.
    
    Returns:
    - sorted_records: The final sorted list of records.
    - trace: An ordered list of execution events (DIVIDE and MERGE operations)
             for visual step-by-step rendering.
    """
    trace: List[Dict[str, Any]] = []
    step_counter = 0

    def _format_summary(sublist: List[Dict[str, Any]]) -> List[str]:
        return [f"{r.get('analysis_id', 'N/A')}: {r.get('final_risk_score', 0.0):.2f}" for r in sublist]

    def _sort_recursive(sublist: List[Dict[str, Any]], depth: int) -> List[Dict[str, Any]]:
        nonlocal step_counter

        if len(sublist) <= 1:
            return list(sublist)

        mid = len(sublist) // 2
        left_sub = sublist[:mid]
        right_sub = sublist[mid:]

        step_counter += 1
        trace.append({
            "step": step_counter,
            "type": "DIVIDE",
            "depth": depth,
            "description": f"Splitting list of size {len(sublist)} at index {mid}",
            "original": _format_summary(sublist),
            "left_part": _format_summary(left_sub),
            "right_part": _format_summary(right_sub),
        })

        sorted_left = _sort_recursive(left_sub, depth + 1)
        sorted_right = _sort_recursive(right_sub, depth + 1)

        merged = _merge_traced(sorted_left, sorted_right, depth)
        return merged

    def _merge_traced(
        left: List[Dict[str, Any]],
        right: List[Dict[str, Any]],
        depth: int
    ) -> List[Dict[str, Any]]:
        nonlocal step_counter
        merged: List[Dict[str, Any]] = []
        i = 0
        j = 0
        comparisons = []

        while i < len(left) and j < len(right):
            comp_str = (
                f"Compare {left[i].get('analysis_id')} ({left[i].get('final_risk_score', 0):.2f}) "
                f"vs {right[j].get('analysis_id')} ({right[j].get('final_risk_score', 0):.2f})"
            )
            if _compare_records(left[i], right[j], descending=descending):
                comparisons.append(f"{comp_str} -> Select Left")
                merged.append(left[i])
                i += 1
            else:
                comparisons.append(f"{comp_str} -> Select Right")
                merged.append(right[j])
                j += 1

        while i < len(left):
            merged.append(left[i])
            i += 1

        while j < len(right):
            merged.append(right[j])
            j += 1

        step_counter += 1
        trace.append({
            "step": step_counter,
            "type": "MERGE",
            "depth": depth,
            "description": f"Merged left ({len(left)} items) and right ({len(right)} items) into {len(merged)} sorted items",
            "left_input": _format_summary(left),
            "right_input": _format_summary(right),
            "comparisons": comparisons,
            "merged_output": _format_summary(merged),
        })

        return merged

    sorted_result = _sort_recursive(records, depth=0)
    return sorted_result, trace

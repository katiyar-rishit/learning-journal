"""
PhishGuard - Custom Binary Search on Indexed Array
Academic Data Structures & Algorithms Implementation

Implements Binary Search on a pre-sorted contiguous array of analysis records by Analysis ID.
Includes full trace instrumentation and academic explanations contrasting
indexed random access vs linked list traversal.
"""

from typing import Any, Dict, List, Optional, Tuple


def binary_search_by_id(
    sorted_records: List[Dict[str, Any]],
    target_id: str
) -> Optional[Dict[str, Any]]:
    """
    Standard Binary Search on an array sorted ascending by 'analysis_id'.
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    low = 0
    high = len(sorted_records) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_id = str(sorted_records[mid].get("analysis_id", ""))

        if mid_id == target_id:
            return sorted_records[mid]
        elif mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None


def binary_search_with_trace(
    sorted_records: List[Dict[str, Any]],
    target_id: str
) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Educational Binary Search that logs every comparison and index shift.
    
    Returns:
    - found_record: Dict of the matching analysis record, or None if not found.
    - trace: List of step dictionaries detailing (step, low, mid, high, mid_val, decision).
    """
    trace: List[Dict[str, Any]] = []
    low = 0
    high = len(sorted_records) - 1
    step = 0

    while low <= high:
        step += 1
        mid = (low + high) // 2
        mid_id = str(sorted_records[mid].get("analysis_id", ""))

        step_info = {
            "step": step,
            "low": low,
            "mid": mid,
            "high": high,
            "sub_array_size": high - low + 1,
            "mid_id": mid_id,
            "target_id": target_id,
        }

        if mid_id == target_id:
            step_info["decision"] = f"MATCH FOUND! '{mid_id}' == '{target_id}' at index {mid}."
            trace.append(step_info)
            return sorted_records[mid], trace
        elif mid_id < target_id:
            step_info["decision"] = f"'{mid_id}' < '{target_id}' -> Search RIGHT half: low = {mid + 1}."
            trace.append(step_info)
            low = mid + 1
        else:
            step_info["decision"] = f"'{mid_id}' > '{target_id}' -> Search LEFT half: high = {mid - 1}."
            trace.append(step_info)
            high = mid - 1

    trace.append({
        "step": step + 1,
        "low": low,
        "mid": -1,
        "high": high,
        "sub_array_size": 0,
        "mid_id": "N/A",
        "target_id": target_id,
        "decision": f"NOT FOUND: low ({low}) exceeded high ({high}). Target does not exist in dataset."
    })
    return None, trace


def prepare_sorted_index_by_id(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Creates an indexed array sorted ascending by analysis_id for binary search.
    
    Academic Note:
    - Converting from linked list to array: O(n) time, O(n) space.
    - Sorting array: O(n log n) time.
    - Subsequent binary searches: O(log n) time per query.
    - Only justified if multiple searches are performed without frequent insertions.
    """
    return sorted(records, key=lambda r: str(r.get("analysis_id", "")))

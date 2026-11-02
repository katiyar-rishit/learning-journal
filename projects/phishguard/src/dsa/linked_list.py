"""
PhishGuard - Custom Singly Linked List for Analysis History
Academic Data Structures & Algorithms Implementation

Implements a Singly Linked List with head and tail references for maintaining
the in-memory email inspection history, supporting O(1) appending, O(n) traversal,
linear search by analysis ID, node deletion, and state inspection for visualization.
"""

from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional
import pandas as pd


class AnalysisNode:
    """A node containing a complete email analysis record and a link to the next record."""

    def __init__(
        self,
        analysis_id: str,
        email_text: str,
        predicted_class: int,
        ml_probability: float,
        rule_score: float,
        final_risk_score: float,
        risk_category: str,
        matched_indicators: Optional[List[Dict[str, Any]]] = None,
        url_findings: Optional[List[Dict[str, Any]]] = None,
        timestamp: Optional[str] = None,
        next_node: Optional["AnalysisNode"] = None,
    ):
        self.analysis_id: str = analysis_id
        self.email_text: str = email_text
        self.predicted_class: int = predicted_class
        self.ml_probability: float = ml_probability
        self.rule_score: float = rule_score
        self.final_risk_score: float = final_risk_score
        self.risk_category: str = risk_category
        self.matched_indicators: List[Dict[str, Any]] = matched_indicators or []
        self.url_findings: List[Dict[str, Any]] = url_findings or []
        self.timestamp: str = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next: Optional["AnalysisNode"] = next_node

    def to_dict(self) -> Dict[str, Any]:
        """Convert node content to a serializable dictionary."""
        return {
            "analysis_id": self.analysis_id,
            "email_text": self.email_text,
            "predicted_class": self.predicted_class,
            "predicted_label": "Phishing" if self.predicted_class == 1 else "Legitimate",
            "ml_probability": round(self.ml_probability, 4),
            "rule_score": round(self.rule_score, 4),
            "final_risk_score": round(self.final_risk_score, 4),
            "risk_category": self.risk_category,
            "matched_indicators_count": len(self.matched_indicators),
            "matched_indicators": self.matched_indicators,
            "url_findings_count": len(self.url_findings),
            "url_findings": self.url_findings,
            "timestamp": self.timestamp,
        }

    def __repr__(self) -> str:
        return f"AnalysisNode(id={self.analysis_id!r}, risk={self.final_risk_score:.2f}, label={self.predicted_class})"


class SinglyLinkedList:
    """
    Singly Linked List with both Head and Tail pointers.
    
    Time Complexity:
    - Append: O(1) (leveraging self._tail)
    - Prepend: O(1)
    - Search by ID: O(n) (requires linear traversal from head)
    - Delete by ID: O(n) (linear scan to locate predecessor, then O(1) pointer adjustment)
    - Traverse: O(n)
    - Clear: O(1)
    
    Space Complexity:
    - O(n) nodes storing analysis payloads and pointer references.
    """

    def __init__(self):
        self._head: Optional[AnalysisNode] = None
        self._tail: Optional[AnalysisNode] = None
        self._size: int = 0

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def append(self, node: AnalysisNode) -> None:
        """
        Append an AnalysisNode to the end of the list in O(1) time using tail reference.
        """
        node.next = None  # Ensure no stale link
        if self.is_empty():
            self._head = node
            self._tail = node
        else:
            assert self._tail is not None
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, node: AnalysisNode) -> None:
        """
        Insert an AnalysisNode at the front of the list in O(1) time.
        """
        if self.is_empty():
            self._head = node
            self._tail = node
        else:
            node.next = self._head
            self._head = node
        self._size += 1

    def search_by_id(self, analysis_id: str) -> Optional[AnalysisNode]:
        """
        Linearly traverse from head to search for node with matching analysis_id.
        Time Complexity: O(n)
        """
        curr = self._head
        while curr is not None:
            if curr.analysis_id == analysis_id:
                return curr
            curr = curr.next
        return None

    def delete_by_id(self, analysis_id: str) -> bool:
        """
        Locate and delete a node with the given analysis_id.
        Updates head, tail, and size appropriately.
        Time Complexity: O(n)
        Returns True if deleted, False if not found.
        """
        if self.is_empty():
            return False

        curr = self._head
        prev: Optional[AnalysisNode] = None

        while curr is not None:
            if curr.analysis_id == analysis_id:
                # Deleting head node
                if prev is None:
                    self._head = curr.next
                    if self._head is None:
                        self._tail = None
                else:
                    prev.next = curr.next
                    if curr == self._tail:
                        self._tail = prev

                curr.next = None
                self._size -= 1
                return True

            prev = curr
            curr = curr.next

        return False

    def clear(self) -> None:
        """Clear all nodes from history."""
        self._head = None
        self._tail = None
        self._size = 0

    def to_list(self) -> List[Dict[str, Any]]:
        """Traverse and return list of analysis dictionaries."""
        records = []
        curr = self._head
        while curr is not None:
            records.append(curr.to_dict())
            curr = curr.next
        return records

    def to_dataframe(self) -> pd.DataFrame:
        """Convert linked list contents to a pandas DataFrame."""
        records = self.to_list()
        if not records:
            return pd.DataFrame()
        return pd.DataFrame(records)

    def get_nodes_view(self) -> List[Dict[str, Any]]:
        """
        Returns structured view of nodes and pointers for UI visualization:
        Head -> Node 1 -> Node 2 -> ... -> Tail -> NULL
        """
        view = []
        curr = self._head
        idx = 0
        while curr is not None:
            ptr_label = curr.next.analysis_id if curr.next else "NULL"
            role = []
            if curr == self._head:
                role.append("HEAD")
            if curr == self._tail:
                role.append("TAIL")
            if not role:
                role.append(f"Node #{idx + 1}")

            view.append({
                "index": idx,
                "role": " & ".join(role),
                "analysis_id": curr.analysis_id,
                "final_risk_score": curr.final_risk_score,
                "risk_category": curr.risk_category,
                "predicted_label": "Phishing" if curr.predicted_class == 1 else "Legitimate",
                "next_ptr": ptr_label,
            })
            idx += 1
            curr = curr.next

        return view

    def __iter__(self) -> Iterator[AnalysisNode]:
        curr = self._head
        while curr is not None:
            yield curr
            curr = curr.next

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"SinglyLinkedList(size={self._size}, head={self._head.analysis_id if self._head else 'None'})"

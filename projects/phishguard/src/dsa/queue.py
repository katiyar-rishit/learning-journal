"""
PhishGuard - Custom FIFO Queue using Linked Nodes
Academic Data Structures & Algorithms Implementation

Implements a First-In-First-Out (FIFO) queue with head and tail pointers
for O(1) enqueue and dequeue operations, used for queuing pending email analyses.
"""

from typing import Any, List, Optional


class EmptyQueueError(Exception):
    """Raised when an operation is performed on an empty queue."""
    pass


class QueueNode:
    """A single linked node within the FIFO Queue."""

    def __init__(self, data: Any, next_node: Optional["QueueNode"] = None):
        self.data: Any = data
        self.next: Optional["QueueNode"] = next_node

    def __repr__(self) -> str:
        return f"QueueNode(data={self.data!r})"


class LinkedQueue:
    """
    Custom FIFO Queue implemented with singly-linked QueueNodes.
    
    Time Complexity:
    - Enqueue: O(1) (tail pointer)
    - Dequeue: O(1) (head pointer)
    - Peek: O(1)
    - IsEmpty: O(1)
    - Size: O(1)
    
    Space Complexity:
    - O(n), where n is the number of queued items.
    """

    def __init__(self):
        self._head: Optional[QueueNode] = None  # Front of queue (dequeue here)
        self._tail: Optional[QueueNode] = None  # Rear of queue (enqueue here)
        self._size: int = 0

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def enqueue(self, item: Any) -> None:
        """
        Add an item to the rear (tail) of the queue in O(1) time.
        """
        new_node = QueueNode(data=item)
        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            assert self._tail is not None
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self) -> Any:
        """
        Remove and return the item from the front (head) of the queue in O(1) time.
        Raises EmptyQueueError if queue is empty.
        """
        if self.is_empty():
            raise EmptyQueueError("Cannot dequeue from an empty queue.")

        assert self._head is not None
        dequeued_data = self._head.data
        self._head = self._head.next
        self._size -= 1

        if self._head is None:
            self._tail = None

        return dequeued_data

    def peek(self) -> Any:
        """
        Inspect the item at the front (head) without removing it in O(1) time.
        Raises EmptyQueueError if queue is empty.
        """
        if self.is_empty():
            raise EmptyQueueError("Cannot peek into an empty queue.")

        assert self._head is not None
        return self._head.data

    def clear(self) -> None:
        """Remove all items from the queue."""
        self._head = None
        self._tail = None
        self._size = 0

    def to_list(self) -> List[Any]:
        """Return list of elements from front (head) to rear (tail)."""
        elements = []
        curr = self._head
        while curr is not None:
            elements.append(curr.data)
            curr = curr.next
        return elements

    def get_queue_view(self) -> List[dict]:
        """
        Returns structured view of nodes from front to rear for UI visualization,
        labeling FRONT, REAR, and index.
        """
        view = []
        curr = self._head
        idx = 0
        while curr is not None:
            role = []
            if idx == 0:
                role.append("FRONT (Dequeue)")
            if idx == self._size - 1:
                role.append("REAR (Enqueue)")
            if not role:
                role.append("Internal")

            view.append({
                "index": idx,
                "role": " & ".join(role),
                "data": curr.data
            })
            idx += 1
            curr = curr.next
        return view

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        curr = self._head
        while curr is not None:
            yield curr.data
            curr = curr.next

    def __repr__(self) -> str:
        return f"LinkedQueue(size={self._size}, front={self._head.data if self._head else None!r})"

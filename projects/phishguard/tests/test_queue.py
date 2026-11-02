"""
Unit tests for custom FIFO LinkedQueue.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dsa.queue import LinkedQueue, EmptyQueueError


def test_queue_enqueue_dequeue_fifo():
    q = LinkedQueue()
    assert q.is_empty() is True
    assert q.size == 0

    q.enqueue("Email 1")
    q.enqueue("Email 2")
    q.enqueue("Email 3")

    assert q.size == 3
    assert q.is_empty() is False
    assert q.peek() == "Email 1"

    # FIFO order: 1, then 2, then 3
    assert q.dequeue() == "Email 1"
    assert q.size == 2
    assert q.dequeue() == "Email 2"
    assert q.size == 1
    assert q.dequeue() == "Email 3"
    assert q.size == 0
    assert q.is_empty() is True


def test_queue_empty_operations():
    q = LinkedQueue()
    with pytest.raises(EmptyQueueError):
        q.dequeue()

    with pytest.raises(EmptyQueueError):
        q.peek()


def test_queue_clear():
    q = LinkedQueue()
    q.enqueue("A")
    q.enqueue("B")
    assert q.size == 2

    q.clear()
    assert q.size == 0
    assert q.is_empty() is True
    with pytest.raises(EmptyQueueError):
        q.peek()


def test_queue_to_list():
    q = LinkedQueue()
    items = ["email_a", "email_b", "email_c"]
    for item in items:
        q.enqueue(item)

    assert q.to_list() == items

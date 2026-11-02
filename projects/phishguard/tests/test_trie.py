"""
Unit tests for SuspiciousPhraseTrie.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dsa.trie import SuspiciousPhraseTrie


def test_trie_insert_and_exact_search():
    trie = SuspiciousPhraseTrie()
    trie.insert("urgent", {"weight": 2.5, "category": "URGENCY"})
    trie.insert("bank details", {"weight": 3.5, "category": "FINANCIAL_SCAM"})

    assert trie.size == 2

    found, meta = trie.search_exact("urgent")
    assert found is True
    assert meta["weight"] == 2.5

    found, meta = trie.search_exact("bank details")
    assert found is True
    assert meta["category"] == "FINANCIAL_SCAM"

    found, meta = trie.search_exact("unknown")
    assert found is False
    assert meta is None


def test_trie_prefix_matching():
    trie = SuspiciousPhraseTrie()
    trie.insert("account")
    trie.insert("account suspended")
    trie.insert("action")

    assert trie.starts_with("acc") is True
    assert trie.starts_with("act") is True
    assert trie.starts_with("xyz") is False

    words = trie.get_words_with_prefix("acc")
    assert "account" in words
    assert "account suspended" in words
    assert len(words) == 2


def test_trie_delete():
    trie = SuspiciousPhraseTrie()
    trie.insert("click here")
    trie.insert("click here to verify")

    assert trie.size == 2
    assert trie.delete("click here") is True
    assert trie.size == 1

    # "click here" is deleted, but "click here to verify" remains
    found, _ = trie.search_exact("click here")
    assert found is False
    found, _ = trie.search_exact("click here to verify")
    assert found is True

    # Delete non-existent
    assert trie.delete("random") is False


def test_trie_avoid_false_substring_matches():
    """
    CRITICAL TEST: Ensure 'urgent' is not matched inside 'detergent',
    and 'bank' is not matched inside 'banking'.
    """
    trie = SuspiciousPhraseTrie()
    trie.insert("urgent", {"weight": 2.5})
    trie.insert("bank", {"weight": 3.0})

    # Email containing words that contain the substring
    clean_email = "Please use gentle laundry detergent when cleaning."
    matches = trie.match_in_text(clean_email)
    assert len(matches) == 0, f"Expected 0 matches in 'detergent', got {matches}"

    clean_email_2 = "We are discussing internet banking regulations."
    matches_2 = trie.match_in_text(clean_email_2)
    assert len(matches_2) == 0, f"Expected 0 matches in 'banking', got {matches_2}"

    # Email with real suspicious term
    suspicious_email = "This is urgent! Please submit immediately."
    matches_3 = trie.match_in_text(suspicious_email)
    assert len(matches_3) == 1
    assert matches_3[0]["term"] == "urgent"
    assert matches_3[0]["original_text"] == "urgent"


def test_trie_multiword_matching():
    trie = SuspiciousPhraseTrie()
    trie.insert("update your billing information", {"weight": 3.5})
    trie.insert("click here", {"weight": 1.8})

    text = "Dear customer, please update your billing information. Click here to confirm."
    matches = trie.match_in_text(text)

    matched_terms = [m["term"] for m in matches]
    assert "update your billing information" in matched_terms
    assert "click here" in matched_terms

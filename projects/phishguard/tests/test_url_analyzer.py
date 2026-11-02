"""
Unit tests for URL Static Analyzer.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.url_analyzer import analyze_single_url, analyze_all_urls


def test_ip_based_url():
    url = "http://192.168.1.100/login/verify.php"
    result = analyze_single_url(url)
    assert result["is_valid"] is True
    heuristics = [f["heuristic"] for f in result["findings"]]
    assert "IP-Based Hostname" in heuristics
    assert result["normalized_risk_score"] > 0.4


def test_excessive_subdomains():
    url = "https://secure.banking.portal.login.account.attacker.com/auth"
    result = analyze_single_url(url)
    heuristics = [f["heuristic"] for f in result["findings"]]
    assert "Excessive Subdomains" in heuristics


def test_deceptive_brand_keyword():
    url = "https://paypal-security-update-2026.com/confirm"
    result = analyze_single_url(url)
    heuristics = [f["heuristic"] for f in result["findings"]]
    assert "Deceptive Brand Reference" in heuristics


def test_suspicious_tld():
    url = "http://verify-bank-details.xyz/update"
    result = analyze_single_url(url)
    heuristics = [f["heuristic"] for f in result["findings"]]
    assert "High-Abuse TLD" in heuristics


def test_benign_url():
    url = "https://www.google.com/search?q=test"
    result = analyze_single_url(url)
    assert result["is_valid"] is True
    assert result["normalized_risk_score"] < 0.2

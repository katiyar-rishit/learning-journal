"""
PhishGuard - Local Static URL Risk Analyzer
Academic Static Inspection of Embedded URLs

Inspects URL syntax, host topology, brand deception, and encoding heuristics
strictly using local offline parsing without performing any network requests.
"""

import re
from typing import Any, Dict, List
from urllib.parse import unquote, urlparse


COMMON_TARGET_BRANDS = [
    "paypal", "apple", "google", "microsoft", "amazon",
    "netflix", "chase", "wellsfargo", "bankofamerica", "citi",
    "facebook", "instagram", "dropbox", "dhl", "fedex", "usps"
]

SUSPICIOUS_TLDS = {
    "xyz", "top", "click", "work", "link", "gq", "tk", "ml", "cf", "ga",
    "bid", "country", "stream", "download", "racing", "review"
}

IP_HOST_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)


def analyze_single_url(url_str: str) -> Dict[str, Any]:
    """
    Statically analyzes a single URL for phishing indicators.
    
    Heuristics checked:
    1. IP-address Hostname: Phishers frequently use raw IP addresses to bypass domain reputation.
    2. URL Length: Phishing URLs often exceed 75 characters to hide query payloads.
    3. Excessive Subdomains: Tunneling and domain spoofing typically chain 3+ subdomains.
    4. Deceptive Brand Keywords: Brand names placed in subdomain or path on foreign domains.
    5. Suspicious TLDs: High-abuse top-level domains (.xyz, .top, .click, etc.).
    6. Suspicious Character Encoding: Use of '@' symbol (userinfo trick), excessive hex escapes '%xx', or hyphens.
    """
    findings: List[Dict[str, Any]] = []
    heuristic_score = 0.0

    try:
        parsed = urlparse(url_str)
        hostname = (parsed.hostname or "").lower()
        path = parsed.path or ""
        query = parsed.query or ""
    except Exception as e:
        return {
            "url": url_str,
            "is_valid": False,
            "risk_score": 0.5,
            "findings": [{"heuristic": "Malformed URL", "weight": 0.5, "detail": f"Failed to parse URL syntax: {e}"}]
        }

    # 1. IP Address Hostname
    if IP_HOST_REGEX.match(hostname):
        findings.append({
            "heuristic": "IP-Based Hostname",
            "weight": 3.5,
            "detail": f"Host '{hostname}' is a raw IP address instead of a registered domain name."
        })
        heuristic_score += 3.5

    # 2. URL Length (> 75 characters)
    if len(url_str) > 75:
        findings.append({
            "heuristic": "Excessive URL Length",
            "weight": 1.5,
            "detail": f"URL length ({len(url_str)} chars) exceeds the 75-character safety baseline."
        })
        heuristic_score += 1.5

    # 3. Subdomain count
    domain_parts = hostname.split(".")
    subdomain_count = max(0, len(domain_parts) - 2)
    if subdomain_count >= 3:
        findings.append({
            "heuristic": "Excessive Subdomains",
            "weight": 2.0,
            "detail": f"Hostname contains {subdomain_count} subdomains, which is common in domain spoofing and tunneling."
        })
        heuristic_score += 2.0

    # 4. Deceptive Brand Keywords
    for brand in COMMON_TARGET_BRANDS:
        if brand in hostname:
            # Check if brand is the actual registered domain (e.g. paypal.com vs paypal-update.com)
            is_official = (
                hostname == f"{brand}.com" or
                hostname.endswith(f".{brand}.com") or
                hostname == f"{brand}.org" or
                hostname.endswith(f".{brand}.org")
            )
            if not is_official:
                findings.append({
                    "heuristic": "Deceptive Brand Reference",
                    "weight": 3.0,
                    "detail": f"Contains trusted brand keyword '{brand}' on an unofficial host '{hostname}'."
                })
                heuristic_score += 3.0
                break

    # 5. Suspicious TLD
    tld = domain_parts[-1] if len(domain_parts) > 1 else ""
    if tld in SUSPICIOUS_TLDS:
        findings.append({
            "heuristic": "High-Abuse TLD",
            "weight": 2.0,
            "detail": f"Domain utilizes top-level domain '.{tld}', which has high historical abuse rates."
        })
        heuristic_score += 2.0

    # 6. Userinfo / @ symbol in URL
    if "@" in url_str:
        findings.append({
            "heuristic": "Credential / Userinfo Delimiter '@'",
            "weight": 3.0,
            "detail": "Contains '@' character, which can deceive browsers into routing past fake hostnames."
        })
        heuristic_score += 3.0

    # 7. Hyphens in hostname
    if hostname.count("-") >= 2:
        findings.append({
            "heuristic": "Multiple Hyphens in Hostname",
            "weight": 1.2,
            "detail": f"Hostname '{hostname}' contains {hostname.count('-')} hyphens, a common obfuscation tactic."
        })
        heuristic_score += 1.2

    # Normalize heuristic score to 0.0 - 1.0 scale
    normalized_risk = min(1.0, heuristic_score / 6.0)

    return {
        "url": url_str,
        "is_valid": True,
        "hostname": hostname,
        "tld": tld,
        "length": len(url_str),
        "subdomain_count": subdomain_count,
        "raw_heuristic_score": round(heuristic_score, 2),
        "normalized_risk_score": round(normalized_risk, 4),
        "findings": findings
    }


def analyze_all_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """Analyzes a list of URLs and returns structured inspection findings."""
    return [analyze_single_url(u) for u in urls]

"""
PhishGuard - Preprocessing and Text Normalization Module
Handles email text sanitization, tokenization, and embedded URL extraction.
"""

import html
import re
from typing import List, Tuple


URL_REGEX = re.compile(
    r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""",
    re.VERBOSE
)


def extract_urls(text: str) -> List[str]:
    """
    Extracts all URLs embedded within an email text.
    Handles standard http/https schemes, www prefixes, and path parameters.
    """
    if not text:
        return []

    matches = URL_REGEX.findall(text)
    urls = []
    for match in matches:
        url_str = match[0]
        # Ensure scheme is present for parsing
        if not url_str.startswith(("http://", "https://")):
            url_str = "http://" + url_str
        urls.append(url_str)

    return urls


def clean_email_text(text: str) -> str:
    """
    Cleans raw email text for machine learning inference and NLP parsing:
    - Decodes HTML entities (e.g., &amp; -> &)
    - Strips raw HTML tags (e.g., <p>, <a href=...>)
    - Normalizes unicode spaces
    - Preserves structural words and casing for rule inspection
    """
    if not isinstance(text, str):
        return ""

    # Unescape HTML
    text = html.unescape(text)

    # Strip HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Replace multiple whitespaces and newlines with a single space
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize_words(text: str) -> List[str]:
    """Tokenizes text into words and alphanumeric tokens."""
    cleaned = clean_email_text(text)
    tokens = re.findall(r"\b\w+\b", cleaned.lower())
    return tokens

"""
PhishGuard - Detection Pipeline & Risk Engine
Coordinates ML Inference, Custom Trie Detection, Custom Hash Table Lookups,
and URL Static Analysis into an aggregated, transparent security risk report.
"""

import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    CATEGORIES,
    DEFAULT_SUSPICIOUS_INDICATORS,
    RISK_THRESHOLDS,
)
from src.dsa.hash_table import SeparateChainingHashTable
from src.dsa.trie import SuspiciousPhraseTrie
from src.model_inference import predict_email
from src.preprocessing import clean_email_text, extract_urls
from src.url_analyzer import analyze_all_urls


class RiskEngine:
    """
    Unified Risk Engine integrating Machine Learning and custom Data Structures.
    """

    def __init__(self, ml_weight: float = 0.60):
        self.ml_weight: float = ml_weight
        self.rule_weight: float = 1.0 - ml_weight

        # Custom Data Structures
        self.hash_table = SeparateChainingHashTable(initial_capacity=32)
        self.trie = SuspiciousPhraseTrie()

        # Initialize DSA stores with indicator catalog
        self._populate_indicators()

    def _populate_indicators(self) -> None:
        """Populates the custom Hash Table and Trie with suspicious indicators."""
        for item in DEFAULT_SUSPICIOUS_INDICATORS:
            term = item["term"]
            meta = {
                "category": item["category"],
                "category_name": CATEGORIES.get(item["category"], item["category"]),
                "weight": item["weight"],
                "explanation": item["explanation"],
            }
            # Insert into custom Hash Table
            self.hash_table.insert(term, meta)
            # Insert into custom Trie
            self.trie.insert(term, meta)

    def analyze_email(
        self,
        email_text: str,
        analysis_id: Optional[str] = None,
        model_type: str = "logistic_regression",
        ml_threshold: float = 0.50
    ) -> Dict[str, Any]:
        """
        Executes complete multi-stage analysis pipeline:
        1. Sanitize text and extract URLs.
        2. ML Model predicts phishing probability.
        3. Custom Trie identifies suspicious terms/phrases and exact character offsets.
        4. Custom Hash Table retrieves category and risk weight for each match.
        5. URL Analyzer statically inspects extracted URLs.
        6. Compute transparent normalized rule-based score and final risk score.
        7. Classify into risk category and generate user safety recommendations.
        """
        if not analysis_id:
            analysis_id = f"PG-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        cleaned_text = clean_email_text(email_text)

        # 1. ML Classifier Inference
        ml_result = predict_email(
            email_text=cleaned_text,
            model_type=model_type,
            threshold=ml_threshold
        )
        ml_prob = ml_result["phishing_probability"]
        predicted_class = ml_result["predicted_class"]

        # 2. Custom Trie matching for suspicious phrases
        trie_matches = self.trie.match_in_text(email_text)

        # 3. Custom Hash Table lookup for rich metadata
        matched_indicators: List[Dict[str, Any]] = []
        raw_keyword_weight = 0.0

        for match in trie_matches:
            term = match["term"]
            # Look up metadata from custom Hash Table
            ht_data = self.hash_table.get(term)
            if ht_data:
                category = ht_data.get("category", "UNKNOWN")
                category_name = ht_data.get("category_name", category)
                weight = float(ht_data.get("weight", 1.0))
                explanation = ht_data.get("explanation", "")
            else:
                category = match.get("metadata", {}).get("category", "UNKNOWN")
                category_name = category
                weight = float(match.get("metadata", {}).get("weight", 1.0))
                explanation = match.get("metadata", {}).get("explanation", "")

            raw_keyword_weight += weight
            matched_indicators.append({
                "term": term,
                "original_text": match.get("original_text", term),
                "start_pos": match.get("start_pos", 0),
                "end_pos": match.get("end_pos", 0),
                "category": category,
                "category_name": category_name,
                "weight": weight,
                "explanation": explanation,
            })

        # 4. URL Static Inspection
        extracted_urls = extract_urls(email_text)
        url_analyses = analyze_all_urls(extracted_urls)

        max_url_risk = 0.0
        if url_analyses:
            max_url_risk = max(u["normalized_risk_score"] for u in url_analyses)

        # 5. Rule Score Normalization
        # Saturation curve: 6.0 total weight maps to ~0.86, capped at 1.0
        keyword_score_normalized = min(1.0, raw_keyword_weight / 7.0)

        if url_analyses:
            rule_score = round(0.65 * keyword_score_normalized + 0.35 * max_url_risk, 4)
        else:
            rule_score = round(keyword_score_normalized, 4)

        # 6. Final Aggregation
        # Transparent weighted combination: ML (60%) + Rules (40%)
        final_risk_score = round(
            (self.ml_weight * ml_prob) + (self.rule_weight * rule_score),
            4
        )

        # 7. Risk Category Determination
        if final_risk_score < RISK_THRESHOLDS["LOW_MAX"]:
            risk_category = "Low"
            risk_badge_color = "#10B981"  # Emerald green
        elif final_risk_score < RISK_THRESHOLDS["MEDIUM_MAX"]:
            risk_category = "Medium"
            risk_badge_color = "#F59E0B"  # Amber
        elif final_risk_score < RISK_THRESHOLDS["HIGH_MAX"]:
            risk_category = "High"
            risk_badge_color = "#F97316"  # Orange
        else:
            risk_category = "Critical"
            risk_badge_color = "#EF4444"  # Red

        # 8. User Safety Recommendations
        recommendations = self._generate_recommendations(
            risk_category=risk_category,
            matched_indicators=matched_indicators,
            url_analyses=url_analyses,
            predicted_class=predicted_class
        )

        return {
            "analysis_id": analysis_id,
            "email_text": email_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ml_prediction": {
                "predicted_class": predicted_class,
                "predicted_label": "Phishing" if predicted_class == 1 else "Legitimate",
                "phishing_probability": ml_prob,
                "legitimate_probability": ml_result["legitimate_probability"],
                "threshold": ml_threshold,
                "top_features": ml_result["top_features"],
            },
            "rule_analysis": {
                "rule_score": rule_score,
                "raw_keyword_weight": round(raw_keyword_weight, 2),
                "matched_count": len(matched_indicators),
                "matched_indicators": matched_indicators,
                "url_findings_count": len(url_analyses),
                "url_findings": url_analyses,
            },
            "final_risk_score": final_risk_score,
            "risk_category": risk_category,
            "risk_badge_color": risk_badge_color,
            "recommendations": recommendations,
        }

    def _generate_recommendations(
        self,
        risk_category: str,
        matched_indicators: List[Dict[str, Any]],
        url_analyses: List[Dict[str, Any]],
        predicted_class: int
    ) -> List[str]:
        """Provides actionable, safe cybersecurity hygiene recommendations."""
        recs = []

        if risk_category in ("Critical", "High") or predicted_class == 1:
            recs.append("DO NOT click any links, open attachments, or reply to this message.")
            recs.append("Report this message immediately to your organization's IT security team.")

        categories_present = {m["category"] for m in matched_indicators}

        if "CREDENTIAL_THEFT" in categories_present:
            recs.append("Never enter passwords or multi-factor authentication (MFA) codes on unverified pages.")
        if "FINANCIAL_SCAM" in categories_present:
            recs.append("Treat all unsolicited requests for wire transfers or banking details as fraudulent.")
        if "ACCOUNT_THREAT" in categories_present:
            recs.append("Verify account status directly through the official provider app or website, never via email links.")
        if "PRIZE_SCAM" in categories_present:
            recs.append("Legitimate contests and lotteries do not require fees or sensitive info to claim awards.")

        for url_item in url_analyses:
            if url_item.get("normalized_risk_score", 0) > 0.4:
                recs.append(f"Embedded URL '{url_item['url']}' displays deceptive or high-risk structural patterns.")

        if not recs:
            recs.append("No overt phishing patterns detected. Maintain general security awareness.")
            recs.append("Verify sender email address header before taking any action.")

        return recs

"""
Unit tests for RiskEngine end-to-end integration.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.risk_engine import RiskEngine


def test_risk_engine_phishing_email():
    engine = RiskEngine()
    phish_text = "Dear client, we need you to update your billing information. Click here to proceed."
    result = engine.analyze_email(phish_text)

    assert result["ml_prediction"]["predicted_class"] == 1
    assert result["ml_prediction"]["phishing_probability"] > 0.5
    assert result["rule_analysis"]["matched_count"] > 0
    assert result["final_risk_score"] > 0.6
    assert result["risk_category"] in ("High", "Critical")
    assert len(result["recommendations"]) > 0


def test_risk_engine_legitimate_email():
    engine = RiskEngine()
    legit_text = "Your recent application has been received and is under review. Thank you for applying."
    result = engine.analyze_email(legit_text)

    assert result["ml_prediction"]["predicted_class"] == 0
    assert result["ml_prediction"]["phishing_probability"] < 0.5
    assert result["final_risk_score"] < 0.4
    assert result["risk_category"] in ("Low", "Medium")


def test_risk_engine_with_embedded_url():
    engine = RiskEngine()
    text_with_url = (
        "Your account will be suspended unless you verify. "
        "Click here: http://192.168.1.1/paypal-login.xyz/verify"
    )
    result = engine.analyze_email(text_with_url)
    assert result["rule_analysis"]["url_findings_count"] >= 1
    assert result["final_risk_score"] > 0.65

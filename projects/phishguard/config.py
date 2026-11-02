"""
PhishGuard - Configuration and Constants
Academic Data Structures & Algorithms and ML Cybersecurity Project
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Dataset details
DATASET_NAME = "lixi0029/phishing-mail"
TRAIN_FILE = RAW_DATA_DIR / "train.csv"
VAL_FILE = RAW_DATA_DIR / "val.csv"
TEST_FILE = RAW_DATA_DIR / "test.csv"
DUPLICATE_REPORT_FILE = REPORTS_DIR / "dataset_quality_report.json"

# Model paths
LOGISTIC_REGRESSION_MODEL_PATH = MODELS_DIR / "logistic_regression_pipeline.joblib"
NAIVE_BAYES_MODEL_PATH = MODELS_DIR / "naive_bayes_pipeline.joblib"
MODEL_METRICS_PATH = MODELS_DIR / "model_metrics.json"

# Label semantics (confirmed by inspection of lixi0029/phishing-mail)
LABEL_MAPPING = {
    0: "Legitimate",
    1: "Phishing"
}

# Suspicious Categories for Rule-Based Indicator Engine
CATEGORIES = {
    "URGENCY": "Urgency & Coercion",
    "CREDENTIAL_THEFT": "Credential Theft",
    "ACCOUNT_THREAT": "Account Threats & Suspension",
    "FINANCIAL_SCAM": "Financial & Advance-Fee Scams",
    "IMPERSONATION": "Brand & Authority Impersonation",
    "PRIZE_SCAM": "Lottery & Prize Scams",
    "ATTACHMENT_LURE": "Suspicious Attachment & Invoice",
    "CALL_TO_ACTION": "Deceptive Call to Action",
}

# Default suspicious indicator dictionary for custom Hash Table & Trie
DEFAULT_SUSPICIOUS_INDICATORS = [
    # Urgency & Coercion
    {"term": "urgent", "category": "URGENCY", "weight": 2.5, "explanation": "Creates false panic to force hasty decisions without verification."},
    {"term": "immediately", "category": "URGENCY", "weight": 2.0, "explanation": "Urges immediate action to bypass critical thinking."},
    {"term": "within 24 hours", "category": "URGENCY", "weight": 2.2, "explanation": "Imposes artificial deadlines often used in phishing attacks."},
    {"term": "act now", "category": "URGENCY", "weight": 2.5, "explanation": "Pressures recipient to act before verifying sender authenticity."},
    
    # Credential Theft
    {"term": "update your billing", "category": "CREDENTIAL_THEFT", "weight": 3.5, "explanation": "Attempts to harvest credit card or billing information."},
    {"term": "billing information", "category": "CREDENTIAL_THEFT", "weight": 3.0, "explanation": "Frequently targeted by credential harvesters."},
    {"term": "verify your details", "category": "CREDENTIAL_THEFT", "weight": 3.2, "explanation": "Lures user to enter sensitive personal or account credentials."},
    {"term": "verify your identity", "category": "CREDENTIAL_THEFT", "weight": 3.2, "explanation": "Pretext for harvesting personal identifying data."},
    {"term": "reset your password", "category": "CREDENTIAL_THEFT", "weight": 3.0, "explanation": "Direct vector for account takeover via fake login portals."},
    {"term": "log in to read", "category": "CREDENTIAL_THEFT", "weight": 2.8, "explanation": "Prompts user to sign into an untrusted site under guise of secure mail."},
    
    # Account Threats
    {"term": "account will be suspended", "category": "ACCOUNT_THREAT", "weight": 3.8, "explanation": "Coercive threat designed to trigger panic and compliance."},
    {"term": "suspended unless", "category": "ACCOUNT_THREAT", "weight": 3.6, "explanation": "Blackmail/ultimatum phrasing characteristic of phishing."},
    {"term": "account has been compromised", "category": "ACCOUNT_THREAT", "weight": 3.5, "explanation": "Phony security alert designed to hijack user credentials."},
    {"term": "unusual activity", "category": "ACCOUNT_THREAT", "weight": 2.8, "explanation": "Spoofs bank/service alerts to provoke hasty verification."},
    {"term": "login attempt from a new device", "category": "ACCOUNT_THREAT", "weight": 2.8, "explanation": "Impersonates security notifications to harvest credentials."},
    
    # Financial Scams
    {"term": "nigeria", "category": "FINANCIAL_SCAM", "weight": 4.0, "explanation": "Classic advance-fee 419 scam keyword."},
    {"term": "prince from nigeria", "category": "FINANCIAL_SCAM", "weight": 4.5, "explanation": "Hallmark phrasing of 419 advance-fee fraud."},
    {"term": "transfer $10 million", "category": "FINANCIAL_SCAM", "weight": 4.2, "explanation": "Extravagant financial promise typical of advance-fee schemes."},
    {"term": "bank details", "category": "FINANCIAL_SCAM", "weight": 3.5, "explanation": "Requests banking coordinates for fraudulent wire transfers or theft."},
    {"term": "wire transfer", "category": "FINANCIAL_SCAM", "weight": 3.0, "explanation": "Non-reversible payment method favored by fraudsters."},
    
    # Prize & Lottery Scams
    {"term": "congratulations! you've won", "category": "PRIZE_SCAM", "weight": 3.8, "explanation": "Unsolicited lottery/gift lures to exploit excitement."},
    {"term": "free gift card", "category": "PRIZE_SCAM", "weight": 3.5, "explanation": "Bait commonly used to capture personal details or survey fees."},
    {"term": "claim it", "category": "PRIZE_SCAM", "weight": 2.5, "explanation": "Call-to-action associated with reward and prize scams."},
    
    # Attachment & Invoices
    {"term": "invoice for the recent purchase", "category": "ATTACHMENT_LURE", "weight": 3.0, "explanation": "Social engineering trick provoking user to open malicious attachment."},
    {"term": "please review and confirm", "category": "ATTACHMENT_LURE", "weight": 2.0, "explanation": "Standard lure accompanying malicious documents or macro spreadsheets."},
    
    # Deceptive Call to Action
    {"term": "click here to proceed", "category": "CALL_TO_ACTION", "weight": 3.0, "explanation": "Generic anchor text concealing phishing destination URLs."},
    {"term": "click here to verify", "category": "CALL_TO_ACTION", "weight": 3.2, "explanation": "Misleading link intended to route user to malicious credential portal."},
    {"term": "click here to claim", "category": "CALL_TO_ACTION", "weight": 3.2, "explanation": "Misleading link driving prize bait."},
    {"term": "click here", "category": "CALL_TO_ACTION", "weight": 1.8, "explanation": "Ambiguous call to action; poor email hygiene, common in phishing."},
    {"term": "secure your account", "category": "CALL_TO_ACTION", "weight": 2.6, "explanation": "Manipulative link text masquerading as security mitigation."}
]

# Risk Thresholds
RISK_THRESHOLDS = {
    "LOW_MAX": 0.30,
    "MEDIUM_MAX": 0.65,
    "HIGH_MAX": 0.85
}

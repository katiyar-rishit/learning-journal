"""
PhishGuard - Model Inference Module
Loads serialized ML pipelines and executes email classification and probability estimation.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np

from config import (
    LOGISTIC_REGRESSION_MODEL_PATH,
    NAIVE_BAYES_MODEL_PATH,
)
from src.preprocessing import clean_email_text

# Global in-memory cache for loaded pipelines
_PIPELINE_CACHE: Dict[str, Any] = {}


def load_model_pipeline(model_type: str = "logistic_regression") -> Any:
    """
    Loads serialized ML pipeline from disk using Joblib.
    Uses in-memory caching to avoid redundant disk I/O on repeated invocations.
    """
    global _PIPELINE_CACHE

    if model_type in _PIPELINE_CACHE:
        return _PIPELINE_CACHE[model_type]

    path = LOGISTIC_REGRESSION_MODEL_PATH if model_type == "logistic_regression" else NAIVE_BAYES_MODEL_PATH
    if not path.exists():
        # Auto-train if not found
        from src.model_training import train_and_evaluate_all
        train_and_evaluate_all()

    pipeline = joblib.load(path)
    _PIPELINE_CACHE[model_type] = pipeline
    return pipeline


def predict_email(
    email_text: str,
    model_type: str = "logistic_regression",
    threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Runs model inference on email text.
    
    Returns:
    - predicted_class: 0 (Legitimate) or 1 (Phishing)
    - phishing_probability: float between 0.0 and 1.0
    - legitimate_probability: float between 0.0 and 1.0
    - top_features: keywords/n-grams in this email with highest model weights
    """
    pipeline = load_model_pipeline(model_type)
    cleaned = clean_email_text(email_text)

    # Calculate probabilities
    probas = pipeline.predict_proba([cleaned])[0]
    legit_prob = float(probas[0])
    phish_prob = float(probas[1])

    predicted_class = 1 if phish_prob >= threshold else 0

    # Extract top contributing features from vectorizer and classifier
    top_features = []
    try:
        vectorizer = pipeline.named_steps["tfidf"]
        classifier = pipeline.named_steps["clf"]

        feature_names = vectorizer.get_feature_names_out()
        tfidf_vec = vectorizer.transform([cleaned]).toarray()[0]

        if hasattr(classifier, "coef_"):
            weights = classifier.coef_[0]
            # Contribution is tfidf * weight
            contributions = tfidf_vec * weights
            nonzero_indices = np.where(tfidf_vec > 0)[0]
            sorted_indices = sorted(nonzero_indices, key=lambda idx: contributions[idx], reverse=True)

            for idx in sorted_indices[:8]:
                feature_word = feature_names[idx]
                contrib = float(contributions[idx])
                top_features.append({
                    "feature": feature_word,
                    "tfidf_value": round(float(tfidf_vec[idx]), 4),
                    "model_weight": round(float(weights[idx]), 4),
                    "contribution": round(contrib, 4),
                    "favors": "Phishing" if contrib > 0 else "Legitimate"
                })
    except Exception:
        pass

    return {
        "model_type": model_type,
        "predicted_class": predicted_class,
        "predicted_label": "Phishing" if predicted_class == 1 else "Legitimate",
        "phishing_probability": round(phish_prob, 4),
        "legitimate_probability": round(legit_prob, 4),
        "threshold_applied": threshold,
        "top_features": top_features,
    }

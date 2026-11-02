"""
Unit tests for Machine Learning Pipeline and Inference.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.model_inference import load_model_pipeline, predict_email


def test_load_model_pipeline():
    lr_pipe = load_model_pipeline("logistic_regression")
    assert lr_pipe is not None
    assert "tfidf" in lr_pipe.named_steps
    assert "clf" in lr_pipe.named_steps

    nb_pipe = load_model_pipeline("naive_bayes")
    assert nb_pipe is not None


def test_predict_email():
    res = predict_email(
        "Hello, I am a prince from Nigeria and I need your help to transfer $10 million."
    )
    assert res["predicted_class"] == 1
    assert res["phishing_probability"] > 0.5
    assert len(res["top_features"]) > 0

    res_legit = predict_email(
        "Your appointment is confirmed for next Tuesday at 2 PM. See you then!"
    )
    assert res_legit["predicted_class"] == 0
    assert res_legit["phishing_probability"] < 0.5

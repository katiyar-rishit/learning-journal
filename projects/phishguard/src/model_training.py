"""
PhishGuard - Model Training and Model Comparison Pipeline
Trains TF-IDF + Logistic Regression and TF-IDF + Multinomial Naive Bayes models,
performs validation-based threshold tuning, evaluates on original test split,
and runs duplicate-aware generalization evaluation.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from config import (
    LOGISTIC_REGRESSION_MODEL_PATH,
    MODEL_METRICS_PATH,
    MODELS_DIR,
    NAIVE_BAYES_MODEL_PATH,
)
from src.dataset_loader import (
    analyze_dataset_quality,
    build_duplicate_aware_split,
    load_raw_dataset,
)
from src.evaluation import compute_comprehensive_metrics
from src.preprocessing import clean_email_text


def build_pipeline(model_type: str = "logistic_regression") -> Pipeline:
    """Creates a Scikit-Learn Pipeline with TF-IDF word unigrams + bigrams."""
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_features=5000,
        preprocessor=clean_email_text,
    )

    if model_type == "logistic_regression":
        classifier = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    elif model_type == "naive_bayes":
        classifier = MultinomialNB(alpha=1.0)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    return Pipeline([
        ("tfidf", vectorizer),
        ("clf", classifier),
    ])


def tune_threshold_on_validation(
    pipeline: Pipeline,
    val_texts: list,
    val_labels: list
) -> Tuple[float, float]:
    """
    Finds the probability threshold on the validation split that maximizes F1 score.
    Never touches the test split!
    """
    probas = pipeline.predict_proba(val_texts)[:, 1]
    best_thresh = 0.5
    best_f1 = -1.0

    # Grid search candidate thresholds from 0.1 to 0.9
    for thresh in np.linspace(0.1, 0.9, 17):
        preds = (probas >= thresh).astype(int)
        metrics = compute_comprehensive_metrics(val_labels, preds.tolist(), probas.tolist(), "Val")
        f1 = metrics["f1_score"]
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = float(thresh)

    return round(best_thresh, 2), round(best_f1, 4)


def train_and_evaluate_all() -> Dict[str, Any]:
    """
    Executes complete academic training workflow:
    1. Loads dataset and conducts quality/duplicate analysis.
    2. Trains Logistic Regression baseline on train split.
    3. Trains Naive Bayes baseline on train split.
    4. Tunes classification threshold on validation split.
    5. Evaluates both models on untouched test split.
    6. Trains and evaluates separate Duplicate-Aware partition.
    7. Persists artifacts and metrics to disk.
    """
    train_df, val_df, test_df = load_raw_dataset()
    quality_report = analyze_dataset_quality(train_df, val_df, test_df)

    X_train = train_df["email"].tolist()
    y_train = train_df["label"].tolist()

    X_val = val_df["email"].tolist()
    y_val = val_df["label"].tolist()

    X_test = test_df["email"].tolist()
    y_test = test_df["label"].tolist()

    # 1. Train Logistic Regression
    lr_pipeline = build_pipeline("logistic_regression")
    lr_pipeline.fit(X_train, y_train)

    lr_best_thresh, lr_val_f1 = tune_threshold_on_validation(lr_pipeline, X_val, y_val)

    # Test evaluation for Logistic Regression
    lr_test_probas = lr_pipeline.predict_proba(X_test)[:, 1]
    lr_test_preds = (lr_test_probas >= lr_best_thresh).astype(int)
    lr_test_metrics = compute_comprehensive_metrics(
        y_test, lr_test_preds.tolist(), lr_test_probas.tolist(), split_name="Original Test Split"
    )

    # 2. Train Naive Bayes
    nb_pipeline = build_pipeline("naive_bayes")
    nb_pipeline.fit(X_train, y_train)

    nb_best_thresh, nb_val_f1 = tune_threshold_on_validation(nb_pipeline, X_val, y_val)

    # Test evaluation for Naive Bayes
    nb_test_probas = nb_pipeline.predict_proba(X_test)[:, 1]
    nb_test_preds = (nb_test_probas >= nb_best_thresh).astype(int)
    nb_test_metrics = compute_comprehensive_metrics(
        y_test, nb_test_preds.tolist(), nb_test_probas.tolist(), split_name="Original Test Split"
    )

    # 3. Duplicate-Aware Evaluation
    dup_train_df, dup_test_df = build_duplicate_aware_split(train_df, val_df, test_df)
    dup_pipeline = build_pipeline("logistic_regression")
    dup_pipeline.fit(dup_train_df["email"].tolist(), dup_train_df["label"].tolist())

    dup_test_probas = dup_pipeline.predict_proba(dup_test_df["email"].tolist())[:, 1]
    dup_test_preds = (dup_test_probas >= 0.5).astype(int)
    dup_test_metrics = compute_comprehensive_metrics(
        dup_test_df["label"].tolist(),
        dup_test_preds.tolist(),
        dup_test_probas.tolist(),
        split_name="Duplicate-Aware Test Partition"
    )

    # Save models
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(lr_pipeline, LOGISTIC_REGRESSION_MODEL_PATH)
    joblib.dump(nb_pipeline, NAIVE_BAYES_MODEL_PATH)

    combined_results = {
        "selected_model": "Logistic Regression",
        "logistic_regression": {
            "validation_threshold": lr_best_thresh,
            "validation_f1": lr_val_f1,
            "original_test_metrics": lr_test_metrics,
        },
        "naive_bayes": {
            "validation_threshold": nb_best_thresh,
            "validation_f1": nb_val_f1,
            "original_test_metrics": nb_test_metrics,
        },
        "duplicate_aware_evaluation": {
            "train_templates_count": dup_train_df["email"].nunique(),
            "train_samples_count": len(dup_train_df),
            "test_templates_count": dup_test_df["email"].nunique(),
            "test_samples_count": len(dup_test_df),
            "metrics": dup_test_metrics,
        },
        "quality_report": quality_report,
    }

    with open(MODEL_METRICS_PATH, "w") as f:
        json.dump(combined_results, f, indent=2)

    return combined_results


if __name__ == "__main__":
    results = train_and_evaluate_all()
    print("Training finished successfully!")
    print(f"LR Test Accuracy: {results['logistic_regression']['original_test_metrics']['accuracy']}")
    print(f"Duplicate-Aware Test Accuracy: {results['duplicate_aware_evaluation']['metrics']['accuracy']}")

"""
PhishGuard - Machine Learning Evaluation Suite
Academic Model Performance Metrics, Confusion Matrices, ROC-AUC, and PR Curves
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def compute_comprehensive_metrics(
    y_true: List[int],
    y_pred: List[int],
    y_proba: List[float],
    split_name: str = "Test"
) -> Dict[str, Any]:
    """
    Computes all standard classification performance metrics:
    - Accuracy, Precision, Recall, F1
    - Confusion Matrix (TN, FP, FN, TP)
    - ROC-AUC and ROC curve coordinates
    - Precision-Recall curve coordinates
    - Exact false positive and false negative counts
    """
    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)
    y_proba_arr = np.array(y_proba)

    acc = float(accuracy_score(y_true_arr, y_pred_arr))
    prec = float(precision_score(y_true_arr, y_pred_arr, zero_division=0))
    rec = float(recall_score(y_true_arr, y_pred_arr, zero_division=0))
    f1 = float(f1_score(y_true_arr, y_pred_arr, zero_division=0))

    # Confusion matrix
    cm = confusion_matrix(y_true_arr, y_pred_arr, labels=[0, 1])
    tn, fp, fn, tp = int(cm[0, 0]), int(cm[0, 1]), int(cm[1, 0]), int(cm[1, 1])

    # ROC AUC & Curves
    roc_auc = None
    roc_points = []
    pr_points = []

    try:
        if len(np.unique(y_true_arr)) > 1:
            roc_auc = float(roc_auc_score(y_true_arr, y_proba_arr))
            fpr, tpr, roc_thresh = roc_curve(y_true_arr, y_proba_arr)
            for f, t, th in zip(fpr.tolist(), tpr.tolist(), roc_thresh.tolist()):
                roc_points.append({"fpr": round(f, 4), "tpr": round(t, 4), "threshold": round(th, 4)})

            prec_pts, rec_pts, pr_thresh = precision_recall_curve(y_true_arr, y_proba_arr)
            for p, r in zip(prec_pts.tolist(), rec_pts.tolist()):
                pr_points.append({"precision": round(p, 4), "recall": round(r, 4)})
    except Exception:
        pass

    return {
        "split_name": split_name,
        "sample_count": len(y_true_arr),
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4) if roc_auc is not None else "N/A",
        "confusion_matrix": {
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp,
            "matrix": [[tn, fp], [fn, tp]]
        },
        "false_positive_count": fp,
        "false_negative_count": fn,
        "roc_curve_samples": roc_points[:50],  # sample points for charts
        "pr_curve_samples": pr_points[:50],
    }

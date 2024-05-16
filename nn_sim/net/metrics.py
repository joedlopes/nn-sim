import numpy as np


def compute_classification_metrics(y_true, y_pred):
    """
    Computes accuracy, precision, recall, and F1-score.

    Args:
    y_true (np.array): Array of true binary labels (0 or 1).
    y_pred (np.array): Array of predicted binary labels (0 or 1).

    Returns:
    dict: Dictionary containing accuracy, recall, precision, and F1-score.
    """

    # Convert predictions to 0 or 1
    y_pred = np.round(y_pred).astype(int)
    y_true = np.round(y_true).astype(int)

    # True positives, false positives, true negatives, false negatives
    TP = np.sum((y_pred == 1) & (y_true == 1))
    FP = np.sum((y_pred == 1) & (y_true == 0))
    TN = np.sum((y_pred == 0) & (y_true == 0))
    FN = np.sum((y_pred == 0) & (y_true == 1))

    # Accuracy
    accuracy = (TP + TN) / (TP + FP + TN + FN) if (TP + FP + TN + FN) != 0 else 0

    # Precision
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0

    # Recall
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0

    # F1-Score
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) != 0
        else 0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
    }

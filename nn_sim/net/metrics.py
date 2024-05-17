import numpy as np


def compute_classification_metrics(y_pred, y_true):
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


def confusion_matrix(y_pred, y_true, threshold=0.5):
    """
    Create a confusion matrix for multi-label data in k-hot encoding format.

    Parameters:
    - y_true (numpy.ndarray): True labels in k-hot encoding.
    - y_pred (numpy.ndarray): Predicted labels in k-hot encoding.

    Returns:
    - numpy.ndarray: A confusion matrix where the element at (i, j) is the number of samples
                      that are labeled as class i by the true labels and as class j by the predictions.
    """
    if y_true.shape != y_pred.shape:
        raise ValueError("Shape of y_true and y_pred must be the same.")

    num_classes = y_true.shape[1]
    confusion_matrix = np.zeros((num_classes, num_classes), dtype=int)

    for i in range(num_classes):
        for j in range(num_classes):
            confusion_matrix[i, j] = np.sum(
                (y_true[:, i] > threshold) & (y_pred[:, j] > threshold)
            )

    return confusion_matrix

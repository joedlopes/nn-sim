import numpy as np


def convert_class_to_1_hot_encoding(labels, n_classes):
    """
    Convert an array of labels to a 1-hot encoded numpy array.

    Parameters:
        labels (np.ndarray): Array of shape (N, 1) containing class indices.
        n_classes (int): Total number of classes.

    Returns:
        np.ndarray: A 1-hot encoded array of shape (N, n_classes).
    """
    # Flatten the array to ensure it's a 1D array for indexing
    labels = labels.flatten()

    # Create a k-hot encoded array using np.eye and indexing
    k_hot_encoded = np.eye(n_classes)[labels]

    return k_hot_encoded

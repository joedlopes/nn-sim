import numpy as np

# regression loss


def sum_of_squared_errors(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    loss = np.sum(0.5 * (y_pred - y_true) ** 2)
    return loss


def sum_of_squared_errors_derivative(
    y_pred: np.ndarray, y_true: np.ndarray
) -> np.ndarray:
    loss = y_pred - y_true
    return loss


def mean_squared_error(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    loss = np.mean((y_pred - y_true) ** 2)
    return loss


def mean_squared_error_derivative(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> np.ndarray:
    N = len(y_pred)
    loss = (2 / N) * (y_pred - y_true)
    return loss


def mean_absolute_error(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    loss = np.mean(np.abs(y_pred - y_true))
    return loss


def mean_absolute_error_derivative(
    y_pred: np.ndarray,
    y_true: np.ndarray,
) -> np.ndarray:
    # MAE has not differentiable when y_pred = y_true (0)
    N = len(y_pred)
    return (1 / N) * np.where(y_pred > y_true, 1, np.where(y_pred < y_true, -1, 0))


# classification loss


def binary_cross_entropy_loss(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> np.ndarray:
    # Clipping prediction values to avoid log(0) error
    epsilon = 1e-12
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    bce_loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return bce_loss


def binary_cross_entropy_loss_derivative(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> np.ndarray:
    epsilon = 1e-12
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -(y_true / y_pred) + (1 - y_true) / (1 - y_pred)


def categorical_cross_entropy(
    y_true: np.ndarray,
    y_pred: np.ndarray,
):
    """
    Compute the categorical cross-entropy loss.

    Parameters:
    - y_true: np.ndarray, one-hot encoded true labels.
    - y_pred: np.ndarray, predicted probabilities for each class.

    Returns:
    - loss: float, the categorical cross-entropy loss.
    """
    # Small epsilon value to prevent undefined log operation
    epsilon = 1e-12
    y_pred = np.clip(y_pred, epsilon, 1.0 - epsilon)
    # Calculate the cross-entropy
    cross_entropy = -np.sum(y_true * np.log(y_pred))
    # Normalize the loss to the number of samples
    loss = np.mean(cross_entropy)
    return loss


def categorical_cross_entropy_derivative(
    y_true: np.ndarray,
    y_pred: np.ndarray,
):
    """
    Compute the derivative of the categorical cross-entropy loss with respect to predictions.

    Parameters:
    - y_true: np.ndarray, one-hot encoded true labels.
    - y_pred: np.ndarray, predicted probabilities for each class.

    Returns:
    - gradients: np.ndarray, derivatives of the loss with respect to each class prediction.
    """
    # Small epsilon value to prevent division by zero
    epsilon = 1e-12
    y_pred = np.clip(y_pred, epsilon, 1.0 - epsilon)
    # Compute the gradient
    gradients = -y_true / y_pred
    return gradients

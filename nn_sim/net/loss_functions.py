import numpy as np


def sum_of_squared_errors(y_est: np.ndarray, y_true: np.ndarray) -> float:
    loss = np.sum(0.5 * (y_est - y_true) ** 2)
    return loss


def sum_of_squared_errors_derivative(y_est: np.ndarray, y_true: np.ndarray) -> np.ndarray:
    loss = (y_est - y_true)
    return loss


def mean_squared_error(y_est: np.ndarray, y_true: np.ndarray) -> float:
    loss = np.mean(2.0 * np.sqrt((y_est - y_true) ** 2))
    return loss


def mean_squared_error_derivative(y_est: np.ndarray, y_true: np.ndarray) -> np.ndarray:
    loss = (y_est - y_true)
    return loss
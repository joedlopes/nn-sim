import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    return x * (1 - x)


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    return np.where(x > 0, 1, 0)


def identity(x: np.ndarray) -> np.ndarray:
    return x.copy(order="C")


def identity_derivative(x: np.ndarray) -> np.ndarray:
    return np.ones_like(x)


def step(x: np.ndarray) -> np.ndarray:
    return np.where(x >= 0, 1, 0)


def step_derivative(x: np.ndarray) -> np.ndarray:
    return np.zeros_like(x)


def softmax(x: np.ndarray) -> np.ndarray:
    e_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
    return e_x / e_x.sum(axis=0)


def softmax_derivative(softmax_output):
    """Compute the Jacobian matrix of softmax output for each output in the softmax."""
    # Reshape the 1-d softmax to 2-d so that np.dot will do the matrix multiplication
    s = softmax_output.reshape(-1, 1)
    return np.diagflat(s) - np.dot(s, s.T)

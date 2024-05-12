import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1 + np.exp(-x))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    return x * (1 - x)


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    x = np.maximum(0, x)
    x[x > 0] = 1.0
    return x


def identity(x: np.ndarray) -> np.ndarray:
    return x.copy(order='C')


def identity_derivative(x: np.ndarray) -> np.ndarray:
    return np.ones_like(x)


def step(x: np.ndarray) -> np.ndarray:
    x = x.copy(order='C')
    x[x <= 0] = 0
    x[x > 0] = 1
    return x


def step_derivative(x: np.ndarray) -> np.ndarray:
    x = x.copy(order='C')
    return x


def softmax(x: np.ndarray) -> np.ndarray:
    return x
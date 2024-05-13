import numpy as np

from . import activation_functions
from . import loss_functions


# Base Module Class


class Module:

    def __init__(self, forward_func, backward_func) -> None:
        self.forward_func = forward_func
        self.backward_func = backward_func

    def __call__(self, *args) -> np.ndarray:
        return self.forward(*args)

    def forward(self, *args) -> np.ndarray:
        return self.forward_func(*args)

    def backward(self, *args) -> np.ndarray:
        return self.backward_func(*args)


# Activation Functions


class Sigmoid(Module):

    def __init__(self) -> None:
        super().__init__(
            activation_functions.sigmoid,
            activation_functions.sigmoid_derivative,
        )


class ReLU(Module):

    def __init__(self) -> None:
        super().__init__(
            activation_functions.relu,
            activation_functions.relu_derivative,
        )


class IdentityActivation(Module):
    def __init__(self) -> None:
        super().__init__(
            activation_functions.identity,
            activation_functions.identity_derivative,
        )


class Step(Module):

    def __init__(self) -> None:
        super().__init__(
            activation_functions.step,
            activation_functions.step_derivative,
        )


class Softmax(Module):

    def __init__(self) -> None:
        super().__init__(
            activation_functions.softmax,
            activation_functions.softmax_derivative,
        )


# loss functions


class SSELoss(Module):

    def __init__(self) -> None:
        super().__init__(
            loss_functions.sum_of_squared_errors,
            loss_functions.sum_of_squared_errors_derivative,
        )


class MSELoss(Module):

    def __init__(self) -> None:
        super().__init__(
            loss_functions.mean_squared_error,
            loss_functions.mean_squared_error_derivative,
        )


class MAELoss(Module):

    def __init__(self) -> None:
        super().__init__(
            loss_functions.mean_absolute_error,
            loss_functions.mean_absolute_error_derivative,
        )


class BinaryCrossEntropyLoss(Module):

    def __init__(self) -> None:
        super().__init__(
            loss_functions.binary_cross_entropy_loss,
            loss_functions.binary_cross_entropy_loss_derivative,
        )


class CategoricalCrossEntropyLoss(Module):

    def __init__(self) -> None:
        super().__init__(
            loss_functions.categorical_cross_entropy,
            loss_functions.categorical_cross_entropy_derivative,
        )


# Linear Layer


class Linear(Module):

    def __init__(
        self,
        n_inputs: int,
        n_outputs: int,
        bias_active: bool,
    ) -> None:
        self.n_inputs: int = n_inputs
        self.n_outputs: int = n_outputs
        self.weights = np.random.randn(n_inputs, n_outputs)
        self.bias = None
        if bias_active:
            self.bias = np.random.randn(n_outputs)

    def forward(self, x: np.ndarray) -> np.ndarray:
        x = x @ self.weights + self.bias
        return x


class HiddenLayer(Module):

    def __init__(
        self,
        n_inputs: int,
        n_outputs: int,
        bias_active: bool,
        activation: Module,
    ) -> None:
        self.weights: np.ndarray = np.random.randn(n_inputs, n_outputs)
        self.bias_active: bool = bias_active
        if bias_active:
            self.bias = np.random.randn(n_outputs)
        self.activation: Module = activation

    def forward(self, x: np.ndarray) -> np.ndarray:
        x = x @ self.weights + self.bias

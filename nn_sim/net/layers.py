import numpy as np

from . import activation_functions
from . import loss_functions


# Base Module Class


class Module:

    def __init__(self, forward_func, diff_func) -> None:
        self.forward_func = forward_func
        self.diff_func = diff_func

    def __call__(self, *args) -> np.ndarray:
        return self.forward(*args)

    def forward(self, *args) -> np.ndarray:
        return self.forward_func(*args)

    def diff(self, *args) -> np.ndarray:
        return self.diff_func(*args)


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


# Loss Function


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


class HiddenLayer(Module):

    def __init__(
        self,
        n_inputs: int,
        n_outputs: int,
        *,
        bias_active: bool,
        activation: Module,
    ) -> None:
        self.weights: np.ndarray = np.random.randn(n_inputs, n_outputs)
        self.bias_active: bool = bias_active
        self.bias = np.random.randn(n_outputs)
        if not bias_active:
            self.bias = np.zeros_like(self.bias)

        self.activation: Module = activation
        self.X = None  # useful for computing gradients
        self.A = None
        self.grad_weights = np.zeros_like(self.weights)
        self.grad_bias = np.zeros_like(self.bias)

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.A_IN = x.copy()  # store inputs for computing gradients

        x = self.activation(x @ self.weights + self.bias)

        self.A_OUT = x.copy()  # store outputs for computing delta
        return x

    def diff(self, delta_in: np.ndarray) -> np.ndarray:
        # compute delta for the layer
        delta = delta_in * self.activation.diff(self.A_OUT)

        # compute gradients
        self.grad_weights += self.A_IN.T @ delta

        self.grad_bias += np.sum(delta, axis=0)

        # compute delta for next layers
        delta_out = delta @ self.weights.T
        return delta_out

    def zero_gradients(self) -> None:
        self.X = None
        self.A = None
        self.grad_weights = np.zeros_like(self.weights)
        self.bias = np.zeros_like(self.bias)

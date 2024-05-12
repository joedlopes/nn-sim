import numpy as np

from . import activation_functions


class Linear:

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


class ActivationFunction:

    def __init__(self, forward_func, backward_func) -> None:
        self.forward_func = forward_func
        self.backward_func = backward_func

    def __call__(self, *args) -> np.ndarray:
        return self.forward(*args)

    def forward(self, x: np.ndarray) -> np.ndarray:
        return self.forward_func(x)

    def backward(self, x: np.ndarray) -> np.ndarray:
        return self.backward_func(x)


class Sigmoid(ActivationFunction):

    def __init__(self) -> None:
        super().__init__(
            activation_functions.sigmoid,
            activation_functions.sigmoid_derivative,
        )

class Sigmoid(ActivationFunction):

    def __init__(self) -> None:
        super().__init__(
            activation_functions.sigmoid,
            activation_functions.sigmoid_derivative,
        )

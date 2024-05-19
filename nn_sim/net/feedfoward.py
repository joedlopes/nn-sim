import numpy as np
from .layers import Module, HiddenLayer


class FeedFowardNeuralNetwork(Module):

    def __init__(
        self,
        n_inputs: int,
        layers: list[tuple[int, bool, Module]],
    ) -> None:
        self.layers: list[HiddenLayer] = []

        for n_neurons, bias_active, activation in layers:
            self.layers.append(
                HiddenLayer(
                    n_inputs,
                    n_neurons,
                    bias_active=bias_active,
                    activation=activation,
                )
            )
            n_inputs = n_neurons

    def forward(self, x: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            x = layer(x)
        return x

    def backward(
        self, y_pred: np.ndarray, y_true: np.ndarray, loss_func: Module
    ) -> np.ndarray:

        delta = loss_func.diff(y_pred, y_true)

        for layer in self.layers[::-1]:
            delta = layer.backward(delta)

    def zero_gradients(self):
        for layer in self.layers:
            layer.zero_gradients()

    def __str__(self) -> str:
        txt = "FeedFowardNeuralNetwork(\n"
        for idx, layer in enumerate(self.layers):
            txt += f"\tLayer [{idx}] Inputs: {layer.weights.shape[0]}, Outputs: {layer.weights.shape[1]}, Activation: {layer.activation.__class__.__name__}\n"
        txt += ")"
        return txt

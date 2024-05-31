import numpy as np
from tqdm import tqdm
from ..data.dataset_loader import DataLoader, DatasetNN
from .layers import Module
from .feedfoward import FeedFowardNeuralNetwork


def train_net_adam(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    train_params: dict[str, str | int | float],
    loss_func: Module,
):
    optim = train_params["optim"]
    epochs = train_params["epochs"]
    mini_batch = train_params["batch_mode"] == "Mini Batch"
    if mini_batch:
        batch_size = train_params["batch_size"]
    learning_rate = train_params["learning_rate"]

    beta1 = train_params["beta1"]
    beta2 = train_params["beta2"]
    epsilon = train_params["epsilon"]

    train_loss, gradients = train_net_adam_grads(
        net,
        dataset,
        learning_rate,
        epochs,
        loss_func,
        beta1,
        beta2,
        epsilon,
    )

    return train_loss, gradients


def train_net_adam_grads(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
    beta1: float,
    beta2: float,
    epsilon: float,
):
    X = dataset.X
    Y = dataset.Y

    # init momentum and velocites
    for layer in net.layers:
        layer.m_weights = np.zeros_like(layer.weights)
        layer.v_weights = np.zeros_like(layer.weights)
        layer.m_bias = np.zeros_like(layer.bias)
        layer.v_bias = np.zeros_like(layer.bias)

    gradients = list()
    train_losses = list()
    for epoch in tqdm(range(epochs)):

        net.zero_gradients()
        y_pred = net(X)
        train_loss = loss_func(y_pred, Y)
        train_losses.append(train_loss)

        # compute gradients
        net.backward(y_pred, Y, loss_func)

        t = epoch + 1  # timestep used for bias correction

        epoch_grads = list()
        gradients.append(epoch_grads)
        for layer in net.layers:

            grads = layer.grad_weights
            if layer.bias_active:
                BIAS_SCALER = 1.0
                grads = np.row_stack((grads, layer.grad_bias * BIAS_SCALER))
            epoch_grads.append(np.abs(grads))

            # Update first moment estimate
            layer.m_weights = beta1 * layer.m_weights + (1 - beta1) * layer.grad_weights
            layer.m_bias = beta1 * layer.m_bias + (1 - beta1) * layer.grad_bias

            # Update second moment estimate
            layer.v_weights = beta2 * layer.v_weights + (1 - beta2) * (
                layer.grad_weights**2
            )
            layer.v_bias = beta2 * layer.v_bias + (1 - beta2) * (layer.grad_bias**2)

            # Compute bias-corrected first and second moment estimates
            m_hat_weights = layer.m_weights / (1 - beta1**t)
            m_hat_bias = layer.m_bias / (1 - beta1**t)
            v_hat_weights = layer.v_weights / (1 - beta2**t)
            v_hat_bias = layer.v_bias / (1 - beta2**t)

            # Update parameters
            layer.weights -= (
                learning_rate * m_hat_weights / (np.sqrt(v_hat_weights) + epsilon)
            )
            layer.bias -= learning_rate * m_hat_bias / (np.sqrt(v_hat_bias) + epsilon)

    print("Train Loss: ", train_loss)
    return train_losses, gradients

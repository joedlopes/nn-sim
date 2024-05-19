import numpy as np
from tqdm import tqdm
from ..data.dataset_loader import DataLoader, DatasetNN
from ..net.layers import Module
from .feedfoward import FeedFowardNeuralNetwork


def train_net(
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
    if optim == "SGD":

        if mini_batch:
            train_net_sgd_mini_batch(
                net,
                dataset,
                learning_rate,
                epochs,
                loss_func,
                batch_size,
            )
        else:
            train_net_sgd(
                net,
                dataset,
                learning_rate,
                epochs,
                loss_func,
            )
    elif optim == "SGD with Momentum":
        momentum = train_params["momentum"]
        if mini_batch:
            train_net_sgd_momentum_mini_batch(
                net,
                dataset,
                learning_rate,
                epochs,
                loss_func,
                batch_size,
                momentum,
            )
        else:
            train_net_sgd_momentum(
                net,
                dataset,
                learning_rate,
                epochs,
                loss_func,
                momentum,
            )
    elif optim == "ADAM":
        beta1 = train_params["beta1"]
        beta2 = train_params["beta2"]
        epsilon = train_params["epsilon"]
        if mini_batch:
            train_net_adam_mini_batch(
                net,
                dataset,
                learning_rate,
                epochs,
                loss_func,
                beta1,
                beta2,
                epsilon,
                batch_size
            )
        else:
            train_net_adam(
                net,
                dataset,
                learning_rate,
                epochs,
                loss_func,
                beta1,
                beta2,
                epsilon
            )


def train_net_sgd(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
):
    X = dataset.X
    Y = dataset.Y
    train_losses = list()
    for epoch in tqdm(range(epochs)):

        net.zero_gradients()
        y_pred = net(X)
        train_loss = loss_func(y_pred, Y)
        train_losses.append(train_loss)

        # compute gradients
        net.backward(y_pred, Y, loss_func)

        # gradient descent update
        for layer in net.layers:
            layer.weights = layer.weights - learning_rate * layer.grad_weights
            layer.bias = layer.bias - learning_rate * layer.grad_bias

    print("Train Loss: ", train_loss)


def train_net_sgd_mini_batch(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
    batch_size: int,
):

    data_loader = DataLoader(dataset, batch_size, True)
    n = len(data_loader)
    train_losses = list()
    for epoch in tqdm(range(epochs)):

        train_loss = 0
        net.zero_gradients()
        for X, Y in data_loader:
            y_pred = net(X)
            train_loss += loss_func(y_pred, Y)

            # compute gradients
            net.backward(y_pred, Y, loss_func)

        train_losses.append(train_loss / n)  # average loss

        # gradient descent update
        for layer in net.layers:
            layer.grad_weights = layer.grad_weights / n
            layer.grad_bias = layer.grad_bias / n

            layer.weights = layer.weights - learning_rate * layer.grad_weights
            layer.bias = layer.bias - learning_rate * layer.grad_bias

    print("Train Loss: ", train_loss)


def train_net_sgd_momentum(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
    momentum: float,
):

    X = dataset.X
    Y = dataset.Y

    # initialize velocity (zeros) for weights and biases for all layers
    for layer in net.layers:
        layer.velocity_weights = np.zeros_like(layer.weights)
        layer.velocity_bias = np.zeros_like(layer.bias)

    train_losses = list()
    for epoch in tqdm(range(epochs)):

        net.zero_gradients()
        y_pred = net(X)
        train_loss = loss_func(y_pred, Y)
        train_losses.append(train_loss)

        # comoput gradients
        net.backward(y_pred, Y, loss_func)

        for layer in net.layers:
            # update velocities
            layer.velocity_weights = momentum * layer.velocity_weights + learning_rate * layer.grad_weights
            layer.velocity_bias = momentum * layer.velocity_bias + learning_rate * layer.grad_bias

            # update parameters
            layer.weights = layer.weights - layer.velocity_weights
            layer.bias = layer.bias - layer.velocity_bias

    print("Train Loss: ", train_loss)


def train_net_sgd_momentum_mini_batch(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
    momentum: float,
    batch_size: int,
):

    data_loader = DataLoader(dataset, batch_size, True)
    n = len(data_loader)

    # initialize velocity (zeros) for weights and biases for all layers
    for layer in net.layers:
        layer.velocity_weights = np.zeros_like(layer.weights)
        layer.velocity_bias = np.zeros_like(layer.bias)

    train_losses = list()
    for epoch in tqdm(range(epochs)):

        train_loss = 0
        net.zero_gradients()
        for X, Y in data_loader:
            y_pred = net(X)
            train_loss += loss_func(y_pred, Y)

            # compute gradients ()
            net.backward(y_pred, Y, loss_func)

        train_losses.append(train_loss / n)  # average loss

        for layer in net.layers:
            layer.grad_weights = layer.grad_weights / n
            layer.grad_bias = layer.grad_bias / n

            # update velocities
            layer.velocity_weights = momentum * layer.velocity_weights + learning_rate * layer.grad_weights
            layer.velocity_bias = momentum * layer.velocity_bias + learning_rate * layer.grad_bias 

            # update parameters
            layer.weights = layer.weights - layer.velocity_weights
            layer.bias = layer.bias - layer.velocity_bias

    print("Train Loss: ", train_loss)


def train_net_adam(
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

    train_losses = list()
    for epoch in tqdm(range(epochs)):

        net.zero_gradients()
        y_pred = net(X)
        train_loss = loss_func(y_pred, Y)
        train_losses.append(train_loss)

        # compute gradients
        net.backward(y_pred, Y, loss_func)

        t = epoch + 1  # timestep used for bias correction

        for layer in net.layers:
            # Update first moment estimate
            layer.m_weights = beta1 * layer.m_weights + (1 - beta1) * layer.grad_weights
            layer.m_bias = beta1 * layer.m_bias + (1 - beta1) * layer.grad_bias

            # Update second moment estimate
            layer.v_weights = beta2 * layer.v_weights + (1 - beta2) * (layer.grad_weights ** 2)
            layer.v_bias = beta2 * layer.v_bias + (1 - beta2) * (layer.grad_bias ** 2)

            # Compute bias-corrected first and second moment estimates
            m_hat_weights = layer.m_weights / (1 - beta1 ** t)
            m_hat_bias = layer.m_bias / (1 - beta1 ** t)
            v_hat_weights = layer.v_weights / (1 - beta2 ** t)
            v_hat_bias = layer.v_bias / (1 - beta2 ** t)

            # Update parameters
            layer.weights -= learning_rate * m_hat_weights / (np.sqrt(v_hat_weights) + epsilon)
            layer.bias -= learning_rate * m_hat_bias / (np.sqrt(v_hat_bias) + epsilon)

    print("Train Loss: ", train_loss)


def train_net_adam_mini_batch(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
    beta1: float,
    beta2: float,
    epsilon: float,
    batch_size: int,
):
    data_loader = DataLoader(dataset, batch_size, True)
    n = len(data_loader)

    # init momentum and velocites
    for layer in net.layers:
        layer.m_weights = np.zeros_like(layer.weights)
        layer.v_weights = np.zeros_like(layer.weights)
        layer.m_bias = np.zeros_like(layer.bias)
        layer.v_bias = np.zeros_like(layer.bias)

    train_losses = list()
    for epoch in tqdm(range(epochs)):

        train_loss = 0
        net.zero_gradients()
        for X, Y in data_loader:
            y_pred = net(X)
            train_loss += loss_func(y_pred, Y)

            # compute gradients ()
            net.backward(y_pred, Y, loss_func)

        train_losses.append(train_loss / n)  # average loss

        t = epoch + 1  # timestep used for bias correction

        for layer in net.layers:
            # gradient averaging
            layer.grad_weights = layer.grad_weights / n
            layer.grad_bias = layer.grad_bias / n

            # Update first moment estimate
            layer.m_weights = beta1 * layer.m_weights + (1 - beta1) * layer.grad_weights
            layer.m_bias = beta1 * layer.m_bias + (1 - beta1) * layer.grad_bias

            # Update second moment estimate
            layer.v_weights = beta2 * layer.v_weights + (1 - beta2) * (layer.grad_weights ** 2)
            layer.v_bias = beta2 * layer.v_bias + (1 - beta2) * (layer.grad_bias ** 2)

            # Compute bias-corrected first and second moment estimates
            m_hat_weights = layer.m_weights / (1 - beta1 ** t)
            m_hat_bias = layer.m_bias / (1 - beta1 ** t)
            v_hat_weights = layer.v_weights / (1 - beta2 ** t)
            v_hat_bias = layer.v_bias / (1 - beta2 ** t)

            # Update parameters
            layer.weights -= learning_rate * m_hat_weights / (np.sqrt(v_hat_weights) + epsilon)
            layer.bias -= learning_rate * m_hat_bias / (np.sqrt(v_hat_bias) + epsilon)

    print("Train Loss: ", train_loss)

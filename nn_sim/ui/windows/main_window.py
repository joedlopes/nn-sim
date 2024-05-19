from ..helpers import uihelper as dc

from ..widgets.property_editor_tree import (
    PropertyItemModel,
    PropertyModel,
    PropertyModelListener,
)

from .model_architecture_widget import ModelArchitectureWidget
from .graph_view_widget import GraphViewWidget
from .dataset_widget import DatasetWidget
from .train_widget import TrainWidget


class MainWindow(dc.QMainWindow, PropertyModelListener):

    def __init__(self, ctx=None) -> None:
        super().__init__()
        self.ctx = ctx

        self.arch_edit = ModelArchitectureWidget()
        self.dock_arch = dc.DockWidget(
            title="Model Architecture", widget=self.arch_edit
        )

        self.graph_view = GraphViewWidget()
        self.dock_graph = dc.DockWidget(title="Graph View", widget=self.graph_view)

        self.arch_edit.on_architecture_changed.connect(self.graph_view.update_graph)

        self.dataset_widget = DatasetWidget()
        self.dock_dataset = dc.DockWidget(title="Dataset", widget=self.dataset_widget)

        self.train_widget = TrainWidget()
        self.dock_train = dc.DockWidget(title="Train", widget=self.train_widget)

        dc.MainWindow(
            widget=self,
            window_ops=dc.WindowOps(
                size=(1000, 800),
                title="nn_sim",
            ),
            docks=[
                (dc.Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_arch),
                (dc.Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_graph),
                (dc.Qt.DockWidgetArea.RightDockWidgetArea, self.dock_dataset),
                (dc.Qt.DockWidgetArea.RightDockWidgetArea, self.dock_train),
            ],
        )

        self.splitDockWidget(
            self.dock_arch, self.dock_graph, dc.Qt.Orientation.Horizontal
        )

        self.dataset_widget.on_dataset_changed.connect(
            self.train_widget.on_dataset_changed
        )
        self.arch_edit.emit_change()

        self.train_widget.btn_start_train.clicked.connect(self.start_training)

    def on_property_item_changed(self, property_item_model: PropertyItemModel) -> None:
        print(property_item_model)

    def on_message(self, message_type: str, message: str) -> None:
        print(message_type, message)

    def on_property_model_changed(self, property_model: PropertyModel) -> None:
        print(property_model)

    def start_training(self) -> None:
        print("Start Training")

        model_info = self.arch_edit.get_model_info()
        dataset = self.dataset_widget.dataset
        if dataset is None:
            dc.Error(
                "Fail to Start Training",
                "Dataset not selected",
                self,
            )
            return

        n_outputs = model_info["arch_n_outputs"]
        n_inputs = model_info["arch_n_inputs"]

        if n_inputs != dataset.X.shape[1]:
            dc.Error(
                "Fail to Start Training",
                "Network input size must match the dataset input size.",
                self,
            )
            return

        if n_outputs != dataset.Y.shape[1]:
            dc.Error(
                "Fail to Start Training",
                "Network output size must match the dataset output size.",
                self,
            )
            return

        # train
        train_params = self.train_widget.get_parameters()
        print(train_params)

        # read last model
        loss_func = get_loss_function_by_name(model_info["arch_loss_function"])

        net = create_net(model_info)
        self.net = net
        print(str(net))

        train_net(net, dataset, train_params, loss_func)


from tqdm import tqdm
from ...net.feedfoward import FeedFowardNeuralNetwork
from ...net.layers import (
    IdentityActivation,
    Sigmoid,
    Step,
    ReLU,
    Module,
    BinaryCrossEntropyLoss,
    SSELoss,
    MSELoss,
    MAELoss,
)
from ...data.dataset_loader import DatasetNN, DataLoader


def get_activation_function_by_name(name: str) -> Module:
    if name == "Identity":
        return IdentityActivation()
    if name == "ReLU":
        return ReLU()
    if name == "Sigmoid":
        return Sigmoid()
    if name == "Step":
        return Step()
    raise AttributeError(f"{name} is not a valid activation function.")


def get_loss_function_by_name(name: str) -> Module:
    if name == "Sum of Squared Errors":
        return SSELoss()
    if name == "Binary Cross Entropy Loss (log-loss)":
        return BinaryCrossEntropyLoss()
    if name == "Mean Squared Error (MSE)":
        return MSELoss()
    if name == "Mean Absolute Error (MAE)":
        return MAELoss()
    raise AttributeError(f"{name} is not a valid loss function.")


def create_net(model_info: dict):

    n_outputs = model_info["arch_n_outputs"]
    n_inputs = model_info["arch_n_inputs"]
    n_hidden = model_info["arch_n_hidden"]
    hidden_layers = model_info["hidden_layers"]

    layers = []
    for idx in range(n_hidden):
        n_neurons = hidden_layers[f"layer_n_neurons_{idx:04d}"]
        has_bias = hidden_layers[f"layer_bias_{idx:04d}"]
        name_act = hidden_layers[f"layer_activation_function_{idx:04d}"]
        activation_function = get_activation_function_by_name(name_act)
        layers.append((n_neurons, has_bias, activation_function))

    has_bias = model_info["arch_output_bias"]
    name_act = model_info["arch_output_activation_function"]
    activation_function = get_activation_function_by_name(name_act)
    layers.append((n_outputs, has_bias, activation_function))
    net = FeedFowardNeuralNetwork(n_inputs, layers)
    return net


def train_net(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    train_params: dict[str, str | int | float],
    loss_func: Module,
):
    epochs = train_params["epochs"]
    mini_batch = train_params["batch_mode"] == "Mini Batch"
    if mini_batch:
        batch_size = train_params["batch_size"]
    learning_rate = train_params["learning_rate"]
    if train_params["optim"] == "SGD":

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

        net.backward(y_pred, Y, loss_func)

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
    pass


def train_net_sgd_momentum(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
):
    pass


def train_net_sgd_momentum_mini_batch(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    loss_func: Module,
):
    pass


def train_net_adam(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    loss_func: Module,
):
    pass


def train_net_adam_mini_batch(
    net: FeedFowardNeuralNetwork,
    dataset: DatasetNN,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    loss_func: Module,
):
    pass

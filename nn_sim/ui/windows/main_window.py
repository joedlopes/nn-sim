import numpy as np

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
from .plot_loss_widget import PlotLossWidget
from .plot_weights_widget import PlotWeightsWidget
from .plot_activations_widget import PlotActivationsWidget

from ...net import train


class MainWindow(dc.QMainWindow, PropertyModelListener):

    def __init__(self, ctx=None) -> None:
        super().__init__()
        self.ctx = ctx
        self.net = None

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

        self.plot_loss = PlotLossWidget()
        self.dock_loss_plot = dc.DockWidget(title="Loss Plot", widget=self.plot_loss)

        self.plot_weights = PlotWeightsWidget()
        self.dock_weights_plot = dc.DockWidget(
            title="Weights Plot", widget=self.plot_weights
        )

        self.plot_activations = PlotActivationsWidget()
        self.dock_activations_plot = dc.DockWidget(
            title="Activations Plot", widget=self.plot_activations
        )

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
                (dc.Qt.DockWidgetArea.RightDockWidgetArea, self.dock_loss_plot),
                (dc.Qt.DockWidgetArea.RightDockWidgetArea, self.dock_weights_plot),
                (dc.Qt.DockWidgetArea.RightDockWidgetArea, self.dock_activations_plot),
            ],
        )

        self.splitDockWidget(
            self.dock_arch, self.dock_graph, dc.Qt.Orientation.Horizontal
        )

        self.splitDockWidget(
            self.dock_graph, self.dock_loss_plot, dc.Qt.Orientation.Vertical
        )

        self.splitDockWidget(
            self.dock_graph, self.dock_weights_plot, dc.Qt.Orientation.Vertical
        )

        self.splitDockWidget(
            self.dock_graph, self.dock_activations_plot, dc.Qt.Orientation.Vertical
        )

        # self.tabifyDockWidget(self.dock_loss_plot, self.dock_weights_plot)

        self.dataset_widget.on_dataset_changed.connect(
            self.train_widget.on_dataset_changed
        )
        self.arch_edit.emit_change()

        self.dataset_widget.select_dataset("./datasets/iris.nnset")

        self.train_widget.btn_start_train.clicked.connect(self.start_training)
        self.dataset_widget.on_sample_changed.connect(
            self.on_dataset_sample_index_changed
        )

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

        loss_train = train.train_net(net, dataset, train_params, loss_func)
        self.plot_loss.set_train_loss(loss_train)

        layers_data = list()
        v_min = None
        v_max = None
        for idx, layer in enumerate(net.layers):
            w = layer.weights
            if layer.bias_active:
                w = np.row_stack((w, layer.bias))
            layers_data.append(w)

            if v_min is None:
                v_min = w.min()
            else:
                v_min = min(w.min(), v_min)
            if v_max is None:
                v_max = w.max()
            else:
                v_max = max(w.max(), v_max)

        self.graph_view.update_net_weights_and_bias(layers_data, v_min, v_max)
        self.plot_weights.update_weights(layers_data)

    def on_dataset_sample_index_changed(self, sample_index: int) -> None:
        if self.net is None:
            dc.Error("Network not trained", "Train the network model first.", self)
            return

        dataset = self.dataset_widget.dataset
        x, y = dataset[sample_index]
        X = np.expand_dims(x, axis=0)
        Y = np.expand_dims(y, axis=0)

        self.net.zero_gradients()
        y_pred = self.net(X)

        neurons_data = [x]
        layers_data = []

        n_min = None
        n_max = None
        v_min = None
        v_max = None
        for layer in self.net.layers:
            # neuros
            neurons_data.append(layer.A_OUT)

            if n_min is None:
                n_min = layer.A_OUT.min()
            else:
                n_min = min(layer.A_OUT.min(), n_min)

            if n_max is None:
                n_max = layer.A_OUT.max()
            else:
                n_max = max(layer.A_OUT.max(), n_max)

            # weights and bias
            ni, no = layer.weights.shape

            print("wx", layer.weights.shape, x.shape)

            aux = np.tile(x.reshape(-1, 1), (1, no))

            w = layer.weights * aux
            x = layer.A_OUT
            if layer.bias_active:
                w = np.row_stack((w, layer.bias))
            layers_data.append(w)

            if v_min is None:
                v_min = w.min()
            else:
                v_min = min(w.min(), v_min)
            if v_max is None:
                v_max = w.max()
            else:
                v_max = max(w.max(), v_max)

        # n_min = min(0.0, n_min)
        # n_max = max(1.0, n_max)
        self.graph_view.update_net_neurons(neurons_data, 0.0, 1.0)
        self.graph_view.update_net_weights_and_bias(layers_data, v_min, v_max)
        self.plot_weights.update_weights(layers_data)
        self.plot_activations.update_activations(neurons_data)


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

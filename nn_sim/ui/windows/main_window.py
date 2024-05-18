from ..helpers import uihelper as dc

from ..widgets.property_editor_tree import (
    PropertyItemModel,
    PropertyModel,
    PropertyModelListener,
    PropertyTreeWidget,
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

        self.splitDockWidget(self.dock_arch, self.dock_graph, dc.Qt.Orientation.Horizontal)

        self.dataset_widget.on_dataset_changed.connect(self.train_widget.on_dataset_changed)
        self.arch_edit.emit_change()

    def on_property_item_changed(self, property_item_model: PropertyItemModel) -> None:
        print(property_item_model)

    def on_message(self, message_type: str, message: str) -> None:
        print(message_type, message)

    def on_property_model_changed(self, property_model: PropertyModel) -> None:
        print(property_model)

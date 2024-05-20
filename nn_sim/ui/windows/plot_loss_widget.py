import pyqtgraph as pg
from ..helpers import uihelper as dc


class PlotLossWidget(dc.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.graph_widget = pg.PlotWidget()
        self.train_plot = self.graph_widget.plot(pen='r', name="Training Loss")
        self.val_plot = self.graph_widget.plot(pen='g', name="Validation Loss")

        self.graph_widget.setLabel('left', "Loss")
        self.graph_widget.setLabel('bottom', "Epoch")
        self.graph_widget.showGrid(x=True, y=True, alpha=0.7)

        self.legend = pg.LegendItem(offset=(-30, 30))
        self.legend.setParentItem(self.graph_widget.graphicsItem())
        self.legend.addItem(self.train_plot, "Training Loss")
        self.legend.addItem(self.val_plot, "Validation Loss")

        dc.Widget(
            widget=self,
            layout=dc.Rows(
                self.graph_widget,
                align=dc.Align.Top,
            )
        )

    def set_validation_loss(self, losses: list[float]) -> None:
        self.val_plot.setData(losses)
        self.graph_widget.autoRange()

    def set_train_loss(self, losses: list[float]) -> None:
        self.train_plot.setData(losses)

        max_val = max(losses)

        self.graph_widget.autoRange()
        self.graph_widget.setYRange(0, max_val)

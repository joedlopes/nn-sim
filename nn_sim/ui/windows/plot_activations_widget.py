import numpy as np
import pyqtgraph as pg
from ..helpers import uihelper as dc


class PlotActivationsWidget(dc.QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.graph_widget = pg.GraphicsLayoutWidget()

        self.plot_items = []

        dc.Widget(
            widget=self,
            layout=dc.Rows(
                self.graph_widget,
                align=dc.Align.Top,
            ),
        )

    def update_activations(self, data: list[np.ndarray]) -> None:
        self.graph_widget.clear()
        self.plot_items = []

        for idx, array in enumerate(data):
            plot_item = self.graph_widget.addPlot(row=0, col=idx)

            array = array.flatten()

            bg = pg.BarGraphItem(
                x=np.arange(len(array)), height=array, width=0.6, brush="b"
            )
            plot_item.addItem(bg)
            if idx == 0:
                plot_item.setTitle(f"Input Layer")
            elif idx == len(data) - 1:
                plot_item.setTitle(f"Output Layer")
            else:
                plot_item.setTitle(f"Layer {idx-1}")

            plot_item.setLabel("left", "Value")
            plot_item.setLabel("bottom", "Index")
            self.plot_items.append(plot_item)

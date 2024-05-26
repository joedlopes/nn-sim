import numpy as np
import pyqtgraph as pg
from ..helpers import uihelper as dc


class BarPlotWidget(dc.QWidget):

    def __init__(self, inputs_as_first_layer=False) -> None:
        super().__init__()
        self.inputs_as_first_layer = inputs_as_first_layer
        self.graph_widget = pg.GraphicsLayoutWidget()
        self.plot_items = []
        dc.Widget(
            widget=self,
            layout=dc.Rows(
                self.graph_widget,
                align=dc.Align.Top,
            ),
        )

    def set_plot_count(self, n: int):
        current_count = len(self.plot_items)
        while current_count < n:
            layer_name = f"Layer {current_count}"
            plot = self.graph_widget.addPlot(title=layer_name)
            if current_count > 0:
                plot.setYLink(self.plot_items[0])
            if current_count == 0:  # Set y-axis label only for the first plot
                plot.setLabel("left", "Value")
            self.plot_items.append(plot)
            current_count += 1
        while current_count > n:
            plot = self.plot_items.pop()
            self.graph_widget.ci.removeItem(plot)
            current_count -= 1

    def update_plots(self, data: list[np.ndarray]) -> None:
        if len(data) != len(self.plot_items):
            self.set_plot_count(len(data))

        for idx, array in enumerate(data):
            plot_item = self.plot_items[idx]

            array = array.flatten()
            bg = pg.BarGraphItem(
                x=np.arange(len(array)), height=array, width=0.6, brush="b"
            )

            if self.inputs_as_first_layer:
                if idx == 0:
                    layer_name = "Input Layer"
                else:
                    layer_name = f"Layer {idx - 1}"
            else:
                layer_name = f"Layer {idx}"

            plot_item.clear()
            plot_item.addItem(bg)
            plot_item.setTitle(layer_name)

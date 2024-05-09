#
# Author: Joed Lopes da Silva
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

from typing import Tuple, Union, List
import numpy as np
from pyqtgraph.opengl import (
    GLTextItem,
    GLScatterPlotItem,
    GLLinePlotItem,
    GLViewWidget,
)
from pyqtgraph import QtGui

from .draw_helper import BaseDrawHelper


class Draw3D(BaseDrawHelper):
    def __init__(
        self,
        scatter_plot: GLScatterPlotItem,
        line_plot: GLLinePlotItem,
        plot_widget: GLViewWidget,
    ) -> None:
        self.scatter_plot: GLScatterPlotItem = scatter_plot
        self.line_plot: GLLinePlotItem = line_plot
        self.plot_widget: GLViewWidget = plot_widget

        self._text_items: List[GLTextItem] = list()

        self.reset()

        self.scale: float = 1.0

    def reset(self, update: bool = True) -> None:
        for item in self._text_items:
            self.plot_widget.removeItem(item)

        self._text_items.clear()

        self._points = np.zeros((0, 3))
        self._points_colors = np.zeros((0, 4))
        self._points_size = np.zeros((0, 1))

        self._lines = np.zeros((0, 3))
        self._lines_colors = np.zeros((0, 4))
        self._lines_size = np.zeros((0, 1))

        if update:
            self.update()

    def update(self) -> None:
        if self._points.shape[0] > 0:
            self.scatter_plot.setData(
                pos=self._points * self.scale,
                color=self._points_colors,
                size=self._points_size.reshape((-1)),
            )
        else:
            self.scatter_plot.setData(
                pos=np.ones((0, 3)), color=(0, 0, 0, 0), size=0.05
            )

        if self._lines.shape[0] > 0:
            self.line_plot.setData(
                pos=self._lines * self.scale, color=self._lines_colors, width=3
            )
        else:
            self.line_plot.setData(
                pos=np.zeros((2, 3)),
                color=(0, 0, 0, 0),
                width=1,
            )

    def point(
        self,
        x: float,
        y: float,
        z: float,
        color: Tuple[float, float, float] = (0, 1, 0, 1),
        point_size: float = 0.05,
        update: bool = True,
    ) -> None:
        self._points = np.vstack(
            (self._points, np.array([[x, y, z]], dtype=np.float32))
        )
        self._points_colors = np.vstack(
            (
                self._points_colors,
                np.array(
                    [[color[0], color[1], color[2], color[3]]],
                    dtype=np.float32,
                ),
            )
        )
        self._points_size = np.vstack(
            (self._points_size, np.array([[point_size]], dtype=np.float32))
        )
        if update:
            self.update()

    def points(
        self,
        points: np.ndarray,
        colors: Union[Tuple[float, float, float, float], np.ndarray] = (
            0.0,
            1.0,
            0.0,
            1.0,
        ),
        points_size: float = 0.05,
        update: bool = True,
    ) -> None:
        self._points = np.vstack((self._points, points))
        sizes = np.tile((points_size), (points.shape[0], 1))
        self._points_size = np.vstack((self._points_size, sizes))

        if isinstance(colors, tuple):
            colors = np.tile(colors, (points.shape[0], 1))
        self._points_colors = np.vstack((self._points_colors, colors))

        if update:
            self.update()

    def line(
        self,
        p1: Tuple[float, float, float],
        p2: Tuple[float, float, float],
        color: Tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
        line_width: float = 1.0,
        update: bool = True,
    ) -> None:
        self._lines = np.vstack(
            (
                self._lines,
                np.array(
                    [
                        [p1[0], p1[1], p1[2]],
                        [p2[0], p2[1], p2[2]],
                    ],
                    dtype=np.float32,
                ),
            )
        )

        self._lines_colors = np.vstack(
            (
                self._lines_colors,
                np.array(
                    [
                        [color[0], color[1], color[2], color[3]],
                        [color[0], color[1], color[2], color[3]],
                    ],
                    dtype=np.float32,
                ),
            )
        )

        self._lines_size = np.vstack(
            (
                self._lines_size,
                np.array([[line_width]], dtype=np.float32),
            )
        )

        if update:
            self.update()

    def lines(
        self,
        line_pts: np.ndarray,
        colors: Tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
        line_width: float = 1.0,
        update: bool = True,
    ) -> None:
        self._lines = np.vstack((self._lines, line_pts))
        sizes = np.tile((line_width), (line_pts.shape[0], 1))
        self._lines_size = np.vstack((self._lines_size, sizes))

        if isinstance(colors, tuple):
            colors = np.tile(colors, (line_pts.shape[0], 1))

        self._lines_colors = np.vstack((self._lines_colors, colors))
        if update:
            self.update()

    def text(
        self,
        x: float,
        y: float,
        z: float,
        text: str,
        text_size: float = 10.0,
        text_color: Tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
        update: bool = True,
    ) -> None:
        assert isinstance(text_color, tuple) or isinstance(text_color, list)
        assert len(text_color) == 4

        r, g, b, a = [int(x * 255) for x in text_color]

        item = GLTextItem(
            pos=(x * self.scale, y * self.scale, z * self.scale),
            color=(r, g, b, a),
            text=text,
            font=QtGui.QFont("Monospace", text_size),
        )

        self.plot_widget.addItem(item)
        self._text_items.append(item)

        if update:
            self.update()

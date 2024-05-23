from ..helpers import uihelper as dc
import numpy as np
import cv2

from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGraphicsLineItem,
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QGraphicsPathItem,
)

# from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen, QPainter, QSurfaceFormat

from PySide6.QtGui import QPen, QPainterPath, QLinearGradient, QColor, QBrush, QPainter
from PySide6.QtCore import Qt, QTimer, QPointF


class FlowingLineItem(QGraphicsPathItem):
    def __init__(self, start_point, end_point):
        super().__init__()
        path = QPainterPath(start_point)
        path.lineTo(end_point)
        self.setPath(path)
        self.gradient = QLinearGradient(start_point, end_point)
        self.gradient.setColorAt(0.0, Qt.red)
        self.gradient.setColorAt(1.0, Qt.blue)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gradient)
        self.timer.start(20)  # Update every 100 ms

    def update_gradient(self):
        # Shift the gradient
        new_stops = [
            ((stop[0] + 0.01) % 1.0, stop[1]) for stop in self.gradient.stops()
        ]
        self.gradient.setStops(new_stops)
        self.update()  # Trigger a repaint

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(QBrush(self.gradient), 2))
        painter.drawPath(self.path())


NEURON_SIZE = 50
NEURON_SIZE_2 = NEURON_SIZE / 2.0

VERTICAL_DISTANCE = 300
HORIZONTAL_DISTANCE = 800

NEURON_PEN_WIDTH = 3
NEURON_PEN_BRUSH = QBrush(QColor(240, 240, 240, 230))
WEIGHT_WIDTH = 5

BRUSH_NEURON = QBrush(QColor(0, 0, 200, 255))
BRUSH_BIAS = QBrush(QColor(200, 200, 0, 255))
BRUSH_WEIGHT = QBrush(QColor(0, 255, 0, 255))

BACKGROUND_BRUSH = QBrush(QColor(5, 5, 10, 255))

COLORMAP = cv2.applyColorMap(
    np.arange(256).astype(np.uint8),
    cv2.COLORMAP_WINTER,
).reshape((-1, 3))

COLORMAP = COLORMAP * np.linspace(0.3, 1.0, 256).reshape(-1, 1)
COLORMAP = COLORMAP.astype(np.uint8)

COLORMAP_NEURONS = cv2.applyColorMap(
    np.arange(256).astype(np.uint8),
    cv2.COLORMAP_OCEAN,
).reshape((-1, 3))


def create_circle(
    x: float,
    y: float,
    size: float,
    brush: QBrush,
    pen: QPen,
    z_value: int = 10,
) -> QGraphicsEllipseItem:
    circle = QGraphicsEllipseItem(x, y, size, size)
    circle.setBrush(brush)
    circle.setPen(pen)
    circle.setZValue(z_value)
    return circle


def create_line(x1, y1, x2, y2, pen, z_value: int = 9) -> QGraphicsLineItem:
    line = QGraphicsLineItem(x1, y1, x2, y2)
    line.setPen(pen)
    line.setZValue(z_value)
    return line


class GraphViewWidget(QGraphicsView):

    def __init__(self) -> None:
        super().__init__()

        # format = QSurfaceFormat.defaultFormat()
        # format.setSamples(32)
        # QSurfaceFormat.setDefaultFormat(format)

        self.setDragMode(QGraphicsView.NoDrag)
        self._isPanning = False
        self._panStartX = 0
        self._panStartY = 0
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._scene.setBackgroundBrush(BACKGROUND_BRUSH)

        self._neurons: list[list[QGraphicsEllipseItem]] = []
        self._biases = []
        self._weights: list[list[QGraphicsLineItem]] = []

    def update_graph(self, model_info: dict) -> None:
        self._neurons.clear()
        self._weights.clear()
        self._biases.clear()
        self._scene.clear()

        n_inputs = model_info["arch_n_inputs"]
        n_outputs = model_info["arch_n_outputs"]
        n_hidden = model_info["arch_n_hidden"]
        layers = [n_inputs]
        biases = []
        for idx in range(n_hidden):
            layers.append(model_info["hidden_layers"][f"layer_n_neurons_{idx:04d}"])
            biases.append(model_info["hidden_layers"][f"layer_bias_{idx:04d}"])
        layers.append(n_outputs)
        biases.append(model_info["arch_output_bias"])

        pen = QPen(Qt.white)
        pen.setWidth(NEURON_PEN_WIDTH)
        pen.setBrush(NEURON_PEN_BRUSH)

        x = 0
        idx_layer = 0
        for n_neurons in layers:
            layer_neurons = list()
            self._neurons.append(layer_neurons)
            y = -n_neurons * VERTICAL_DISTANCE / 2.0

            for _ in range(n_neurons):
                circle = create_circle(x, y, NEURON_SIZE, BRUSH_NEURON, pen, 10)
                self._scene.addItem(circle)
                layer_neurons.append(circle)
                y += VERTICAL_DISTANCE

            if len(biases) > idx_layer and biases[idx_layer]:
                circle = create_circle(
                    x + NEURON_SIZE * 2, y, NEURON_SIZE, BRUSH_BIAS, pen, 10
                )
                self._scene.addItem(circle)
                self._biases.append(circle)
            else:
                self._biases.append(None)

            x += HORIZONTAL_DISTANCE
            idx_layer += 1

        pen_weight = QPen(Qt.white)
        pen_weight.setWidth(WEIGHT_WIDTH)
        pen_weight.setBrush(BRUSH_WEIGHT)

        for idx_layer in range(len(self._neurons) - 1):
            weights = list()
            self._weights.append(weights)
            for n1 in self._neurons[idx_layer]:
                for n2 in self._neurons[idx_layer + 1]:
                    line = create_line(
                        n1.rect().center().x(),
                        n1.rect().center().y(),
                        n2.rect().center().x(),
                        n2.rect().center().y(),
                        pen_weight,
                        9,
                    )
                    line.weight_value = 1.0
                    self._scene.addItem(line)
                    weights.append(line)

            if len(biases) > idx_layer and biases[idx_layer] is True:
                b = self._biases[idx_layer]
                for n2 in self._neurons[idx_layer + 1]:
                    line = create_line(
                        b.rect().center().x(),
                        b.rect().center().y(),
                        n2.rect().center().x(),
                        n2.rect().center().y(),
                        pen_weight,
                        9,
                    )
                    self._scene.addItem(line)
                    weights.append(line)

        rect = self._scene.itemsBoundingRect()
        rect.setLeft(-HORIZONTAL_DISTANCE)
        rect.setRight(rect.right() + HORIZONTAL_DISTANCE)
        self._scene.setSceneRect(rect)
        self.fitInView(rect, Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        scaleFactor = 1.10  # Zoom factor
        if event.angleDelta().y() > 0:  # Zoom in
            self.scale(scaleFactor, scaleFactor)
        else:  # Zoom out
            self.scale(1 / scaleFactor, 1 / scaleFactor)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._isPanning = True
            self._panStartX, self._panStartY = (
                event.position().x(),
                event.position().y(),
            )
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._isPanning:
            # Calculate the new scroll positions
            deltaX = event.position().x() - self._panStartX
            deltaY = event.position().y() - self._panStartY
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - deltaX
            )
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - deltaY)
            self._panStartX, self._panStartY = (
                event.position().x(),
                event.position().y(),
            )
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self._isPanning = False
            self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def update_net_weights_and_bias(
        self,
        layers_data: list[np.ndarray],
        v_min: float = 0.0,
        v_max: float = 1.0,
    ):
        """update the edges (weights) from neurons
        layers_data: [
            np.ndarray - array including bias in the last row,
        ]
        """
        n = len(self._weights)

        assert n == len(layers_data), "Invalida Layer Data"
        pen = QPen()
        pen.setWidth(WEIGHT_WIDTH)

        for layer_idx in range(n):
            wb = layers_data[layer_idx].flatten()
            # v_min = wb.min()
            # v_max = wb.max()
            for idx, line in enumerate(self._weights[layer_idx]):
                line.weight_value = wb[idx]
                v = (wb[idx] - v_min) / (v_max - v_min)
                v = min(max(v, 0.0), 1.0)
                vc = COLORMAP[int(v * 255)]
                pen.setBrush(QBrush(QColor(vc[2], vc[1], vc[0], 255)))
                line.setPen(pen)

    def update_net_neurons(
        self,
        neurons_data: list[np.ndarray],
        v_min: float = 0.0,
        v_max: float = 1.0,
    ):
        for idx_layer, neuron_layers in enumerate(self._neurons):
            activations = neurons_data[idx_layer].flatten()
            print(idx_layer, activations)

            for idx_neuron, neuron in enumerate(neuron_layers):
                v = (activations[idx_neuron] - v_min) / (v_max - v_min)
                v = min(max(v, 0.0), 1.0)
                vc = COLORMAP_NEURONS[int(v * 255)]
                neuron.setBrush(QBrush(QColor(vc[2], vc[1], vc[0], 255)))

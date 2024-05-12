from ..helpers import uihelper as dc

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

VERTICAL_DISTANCE = 200
HORIZONTAL_DISTANCE = 500

NEURON_PEN_WIDTH = 3
NEURON_PEN_BRUSH = QBrush(QColor(255, 255, 255, 200))
WEIGHT_WIDTH = 2

BRUSH_NEURON = QBrush(QColor(0, 0, 200, 255))
BRUSH_WEIGHT = QBrush(QColor(0, 255, 0, 255))


class GraphViewWidget(QGraphicsView):

    def __init__(self) -> None:
        super().__init__()

        format = QSurfaceFormat.defaultFormat()
        format.setSamples(16)
        QSurfaceFormat.setDefaultFormat(format)

        # self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.NoDrag)
        self._isPanning = False
        self._panStartX = 0
        self._panStartY = 0
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        # self.setViewport(QOpenGLWidget())

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._scene.setBackgroundBrush(QBrush(QColor(0, 0, 0, 255)))

        pen = QPen(Qt.white)
        pen.setWidth(3)
        pen.setBrush(QBrush(QColor(255, 255, 255, 255)))

        circle1 = QGraphicsEllipseItem(0, 0, NEURON_SIZE, NEURON_SIZE)
        circle1.setBrush(QBrush(QColor(0, 0, 255, 100)))
        circle1.setPen(pen)
        self._scene.addItem(circle1)

        circle2 = QGraphicsEllipseItem(300, 0, NEURON_SIZE, NEURON_SIZE)
        circle2.setBrush(QBrush(QColor(0, 0, 255, 100)))
        circle2.setPen(pen)
        self._scene.addItem(circle2)

        self._neurons = []
        self._weights = []

    def update_graph(self, model_info: dict) -> None:
        self._neurons.clear()
        self._weights.clear()
        self._scene.clear()

        n_inputs = model_info["arch_n_inputs"]
        n_outputs = model_info["arch_n_outputs"]
        n_hidden = model_info["arch_n_hidden"]
        layers = [n_inputs]
        for idx in range(n_hidden):
            layers.append(model_info["hidden_layers"][f"layer_n_neurons_{idx:04d}"])
        layers += [n_outputs]

        pen = QPen(Qt.white)
        pen.setWidth(NEURON_PEN_WIDTH)
        pen.setBrush(QBrush(QColor(255, 255, 255, 255)))

        x = 0
        for n_neurons in layers:
            layer_neurons = list()
            self._neurons.append(layer_neurons)
            y = -n_neurons * VERTICAL_DISTANCE / 2.0
            for _ in range(n_neurons):
                circle = QGraphicsEllipseItem(x, y, NEURON_SIZE, NEURON_SIZE)
                circle.setBrush(BRUSH_NEURON)
                circle.setPen(pen)
                circle.setZValue(10)
                self._scene.addItem(circle)
                layer_neurons.append(circle)
                y += VERTICAL_DISTANCE
            x += HORIZONTAL_DISTANCE

        pen_weight = QPen(Qt.white)
        pen_weight.setWidth(WEIGHT_WIDTH)
        pen_weight.setBrush(BRUSH_WEIGHT)

        for idx_layer in range(len(self._neurons) - 1):

            weights = list()
            self._weights.append(weights)

            for n1 in self._neurons[idx_layer]:
                for n2 in self._neurons[idx_layer + 1]:

                    line = QGraphicsLineItem(
                        n1.rect().center().x(),
                        n1.rect().center().y(),
                        n2.rect().center().x(),
                        n2.rect().center().y(),
                    )

                    # line = FlowingLineItem(n1.rect().center(), n2.rect().center())

                    line.setPen(pen_weight)
                    line.setZValue(9)
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
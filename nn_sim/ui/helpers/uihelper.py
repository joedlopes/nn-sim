#
# Author: Joed Lopes da Silva
# This library is licensed under MIT License
#
# Copyright Joed 2023
#

from typing import List, Tuple, Union, Optional, Sequence

import os

from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore


from PySide6.QtWidgets import (
    QPushButton,
    QToolButton,
    QWidget,
    QApplication,
    QLineEdit,
    QLabel,
    QTextEdit,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QScrollArea,
    QMainWindow,
    QLayout,
    QDockWidget,
    QMenu,
    QMenuBar,
    QToolBar,
    QStatusBar,
    QCheckBox,
    QRadioButton,
    QTreeWidget,
    QTreeWidgetItem,
    QSpinBox,
    QDoubleSpinBox,
    QFrame,
    QMessageBox,
    QErrorMessage,
    QColorDialog,
    QFileDialog,
    QComboBox,
    QSlider,
    QSpacerItem,
    QStackedWidget,
    QSizePolicy,
    QSplitter,
    QListView,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QGroupBox,
)

from PySide6.QtGui import (
    QIcon,
    QAction,
    QColor,
    QPixmap,
    QPainter,
    QFont,
    QFontDatabase,
    QKeySequence,
)

from PySide6.QtCore import (
    Slot,
    Qt,
    QSize,
    Signal,
    QObject,
    QKeyCombination,
)

from pydantic import BaseModel
from pydantic.types import PositiveInt

from typing import Final

__all__ = [
    "QFont",
    "QFontDatabase",
    "QtWidgets",
    "QtGui",
    "QtCore",
    "Signal",
    "QObject",
    "QHeaderView",
    "QAbstractItemView",
    "QTabWidget",
]

# Size properties


class SizePolicy:
    Expanding: Final = QSizePolicy.Expanding
    Maximum: Final = QSizePolicy.Maximum
    Minimum: Final = QSizePolicy.Minimum
    Preferred: Final = QSizePolicy.Preferred
    Fixed: Final = QSizePolicy.Fixed


class SizeOps(BaseModel):
    min_width: Optional[PositiveInt] = None
    max_width: Optional[PositiveInt] = None
    min_height: Optional[PositiveInt] = None
    max_height: Optional[PositiveInt] = None


def size_ops_set(widget: QWidget, options: Optional[SizeOps] = None) -> None:
    if options is None:
        return

    func_map = dict(
        min_width=widget.setMinimumWidth,
        max_width=widget.setMaximumWidth,
        min_height=widget.setMinimumHeight,
        max_height=widget.setMaximumHeight,
    )

    for key, val in options.dict(exclude_unset=True).items():
        func_map[key](val)


# Window Properties


class WindowOps(BaseModel):
    size: Tuple[PositiveInt, PositiveInt] = None
    title: Optional[str] = None


def window_ops_set(
    widget: QWidget,
    options: Optional[WindowOps] = None,
) -> None:
    if options is None:
        return

    func_map = dict(
        size=widget.resize,
        title=widget.setWindowTitle,
    )

    for key, val in options.dict(exclude_unset=True).items():
        if isinstance(val, tuple):
            func_map[key](*val)
        else:
            func_map[key](val)


# Base sets


def set_widget_object_name(
    widget: QWidget,
    object_name: Optional[str],
) -> None:
    if isinstance(object_name, str):
        widget.setObjectName(object_name)


def set_widget_style_sheet(widget: QWidget, css: Optional[str] = None) -> None:
    if isinstance(css, str):
        widget.setStyleSheet(css)


def set_widget_text(widget, text: str) -> None:
    if isinstance(text, str):
        widget.setText(text)


def set_widget_tooltip(
    widget,
    tooltip_text: str,
    tooltip_duration: Optional[int] = None,
) -> None:
    if isinstance(tooltip_text, str):
        widget.setToolTip(tooltip_text)

    if tooltip_duration is not None:
        widget.setToolTipDuration(int)


def set_widget_shortcut(widget, shortcut: str) -> None:
    if isinstance(shortcut, str):
        widget.setShortcut(shortcut)


def set_widget_icon(
    widget,
    icon: QIcon,
    icon_size: Optional[Tuple[int, int]] = None,
) -> None:
    if isinstance(icon, QIcon):
        widget.setIcon(icon)

        if isinstance(icon_size, tuple) and len(icon_size) == 2:
            widget.setIconSize(QSize(icon_size[0], icon_size[0]))


# Widgets


def Button(
    text: Optional[str] = None,
    *,
    widget: Optional[QPushButton] = None,
    object_name: Optional[str] = None,
    on_click: Optional[Slot] = None,
    icon: Optional[QIcon] = None,
    icon_size: Optional[Tuple[int, int]] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
    shortcut: Optional[str] = None,
    tooltip: Optional[str] = None,
    tooltip_duration_ms: Optional[int] = None,
) -> QPushButton:
    if widget is None:
        widget = QPushButton()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    set_widget_text(widget, text)
    set_widget_icon(widget, icon, icon_size)
    set_widget_shortcut(widget, shortcut)
    size_ops_set(widget, size_ops)
    set_widget_tooltip(widget, tooltip, tooltip_duration_ms)

    if on_click is not None:
        widget.clicked.connect(on_click)

    return widget


def ToolButton(
    text: Optional[str] = None,
    button_style: Optional[
        Qt.ToolButtonStyle
    ] = Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
    *,
    widget: Optional[QToolButton] = None,
    object_name: Optional[str] = None,
    on_click: Optional[Slot] = None,
    icon: Optional[QIcon] = None,
    icon_size: Optional[Tuple[int, int]] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
    shortcut: Optional[str] = None,
    tooltip: Optional[str] = None,
    tooltip_duration_ms: Optional[int] = None,
) -> QToolButton:
    if widget is None:
        widget = QToolButton()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    set_widget_text(widget, text)
    set_widget_icon(widget, icon, icon_size)
    set_widget_shortcut(widget, shortcut)
    size_ops_set(widget, size_ops)
    set_widget_tooltip(widget, tooltip, tooltip_duration_ms)

    if button_style is not None:
        widget.setToolButtonStyle(button_style)

    if on_click is not None:
        widget.clicked.connect(on_click)

    return widget


def Label(
    text: Optional[str] = None,
    *,
    widget: Optional[QLabel] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
    pixmap: Optional[QPixmap] = None,
    alignment: Optional[int] = None,
) -> QLabel:
    if widget is None:
        widget = QLabel()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    set_widget_text(widget, text)
    size_ops_set(widget, size_ops)

    if isinstance(pixmap, QPixmap):
        widget.setPixmap(pixmap)

    if text is not None:
        widget.setText(text)

    if alignment is not None:
        widget.setAlignment(alignment)

    return widget


def SpinBox(
    *,
    range: Optional[Tuple[int, int]] = (0, 1000),
    value: int = 1,
    single_step: int = 1,
    on_value_changed: Optional[Slot] = None,
    widget: Optional[QSpinBox] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QSpinBox:
    if widget is None:
        widget = QSpinBox()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if isinstance(range, tuple):
        assert len(range) == 2, "Range must have a min and max value"
        widget.setRange(range[0], range[1])

    if single_step is not None:
        widget.setSingleStep(single_step)

    if value is not None:
        widget.setValue(value)

    if on_value_changed is not None:
        widget.valueChanged.connect(on_value_changed)

    return widget


def DoubleSpinBox(
    *,
    decimals: int = 3,
    range: Optional[Tuple[int, int]] = (0, 1000),
    value: int = 1,
    single_step: int = 1,
    widget: Optional[QDoubleSpinBox] = None,
    on_value_changed: Optional[Slot] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QDoubleSpinBox:
    if widget is None:
        widget = QDoubleSpinBox()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if isinstance(range, tuple):
        widget.setRange(range[0], range[1])

    if decimals is not None:
        widget.setDecimals(decimals)

    if single_step is not None:
        widget.setSingleStep(single_step)

    if value is not None:
        widget.setValue(value)

    if on_value_changed is not None:
        widget.valueChanged.connect(on_value_changed)

    return widget


def LineEdit(
    text: Optional[str] = "",
    *,
    placeholder_text: Optional[str] = "",
    max_length: Optional[int] = None,
    mask: Optional[str] = None,
    on_return_pressed: Optional[Slot] = None,
    on_text_changed: Optional[Slot] = None,
    widget: Optional[QLineEdit] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    read_only: Optional[bool] = None,
    css: Optional[str] = None,
) -> QLineEdit:
    if widget is None:
        widget = QLineEdit()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    set_widget_text(widget, text)
    size_ops_set(widget, size_ops)

    if placeholder_text is not None:
        widget.setPlaceholderText(placeholder_text)

    if mask is not None:
        widget.setMask(mask)

    if max_length is not None:
        widget.setMaxLength(max_length)

    if on_return_pressed is not None:
        widget.returnPressed.connect(on_return_pressed)

    if on_text_changed is not None:
        widget.textChanged.connect(on_text_changed)

    if read_only is not None:
        widget.setReadOnly(read_only)

    return widget


def CheckBox(
    text: Optional[str] = None,
    *,
    checked: bool = False,
    on_released: Optional[Slot] = None,  # change the type annotation
    on_state_changed: Optional[Slot] = None,
    widget: Optional[QCheckBox] = None,
    object_name: Optional[str] = None,
    icon: Optional[QIcon] = None,
    icon_size: Optional[Tuple[int, int]] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QCheckBox:
    if widget is None:
        widget = QCheckBox()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    set_widget_text(widget, text)
    set_widget_icon(widget, icon, icon_size)
    size_ops_set(widget, size_ops)

    widget.setChecked(checked)

    if on_released is not None:
        widget.released.connect(on_released)

    if on_state_changed is not None:
        widget.stateChanged.connect(on_state_changed)

    return widget


def ComboBox(
    *,
    selected_item: Optional[str] = None,
    items: Optional[List[str]] = None,
    on_index_changed: Optional[Slot] = None,
    widget: Optional[QComboBox] = None,
    object_name: Optional[str] = None,
    icon: Optional[QIcon] = None,
    icon_size: Optional[Tuple[int, int]] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QComboBox:
    if widget is None:
        widget = QComboBox()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    set_widget_icon(widget, icon, icon_size)
    size_ops_set(widget, size_ops)

    selected_index: int = 0
    if isinstance(items, list):
        for i, item in enumerate(items):
            assert isinstance(item, str), "Item must be a string type."
            widget.addItem(item)

            if item == selected_item:
                selected_index = i

    widget.setCurrentIndex(selected_index)

    if on_index_changed is not None:
        widget.currentIndexChanged.connect(on_index_changed)

    return widget


def TextEdit(
    text: Optional[str] = "",
    *,
    placeholder_text: Optional[str] = "",
    max_length: Optional[int] = None,
    on_text_changed: Optional[Slot] = None,
    widget: Optional[QTextEdit] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QTextEdit:
    if widget is None:
        widget = QTextEdit()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    set_widget_text(widget, text)
    size_ops_set(widget, size_ops)

    if placeholder_text is not None:
        widget.setPlaceholderText(placeholder_text)

    if max_length is not None:
        widget.setMaxLength(max_length)

    if on_text_changed is not None:
        widget.textChanged.connect(on_text_changed)

    return widget


def Slider(
    *,
    value: Optional[int] = None,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    tick_interval: Optional[int] = None,
    tick_position: Optional[QSlider.TickPosition] = None,
    on_release: Optional[Slot] = None,
    orientation: Optional[Qt.Orientation] = Qt.Orientation.Horizontal,
    widget: Optional[QSlider] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QSlider:
    if widget is None:
        widget = QSlider()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if tick_interval is not None:
        widget.setTickInterval(tick_interval)

    if minimum is not None:
        widget.setMinimum(minimum)

    if maximum is not None:
        widget.setMaximum(maximum)

    if orientation is not None:
        widget.setOrientation(orientation)

    if tick_position is not None:
        widget.setTickPosition(tick_position)

    if value is not None:
        widget.setValue(value)

    if on_release is not None:
        widget.sliderReleased.connect(on_release)

    return widget


def RadioButton() -> QRadioButton:
    return QRadioButton()


def ListView(
    *,
    widget: Optional[QListView] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QListView:
    if widget is None:
        widget = QListView()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    return widget


def TableWidget(
    *,
    widget: Optional[QTableWidget] = None,
    row_count: Optional[int] = None,
    col_count: Optional[int] = None,
    horizontal_labels: Optional[List[str]] = None,
    stretch_last_section: Optional[bool] = None,
    section_resize_mode: Optional[List[Tuple[int, int]]] = None,
    selection_behavior: Optional[int] = None,
    selection_mode: Optional[int] = None,
    column_item_delegates: Optional[List[Tuple[int, QtWidgets.QItemDelegate]]] = None,
    on_item_changed: Optional[Slot] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QTableWidget:
    if widget is None:
        widget = QTableWidget()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if row_count is not None:
        widget.setRowCount(row_count)
    if col_count is not None:
        widget.setColumnCount(col_count)
    if horizontal_labels is not None:
        widget.setHorizontalHeaderLabels(horizontal_labels)
    if stretch_last_section is not None:
        widget.horizontalHeader().setStretchLastSection(stretch_last_section)
    if section_resize_mode is not None:
        for col, resize_mode in section_resize_mode:
            widget.horizontalHeader().setSectionResizeMode(col, resize_mode)
    if selection_behavior is not None:
        widget.setSelectionBehavior(selection_behavior)
    if selection_mode is not None:
        widget.setSelectionMode(selection_mode)
    if column_item_delegates is not None:
        for col, item_delegate in column_item_delegates:
            widget.setItemDelegateForColumn(0, item_delegate)
    if on_item_changed is not None:
        widget.itemChanged.connect(on_item_changed)

    return widget


def TableWidgetItem(
    text: Optional[str] = None,
    *,
    widget: Optional[QSlider] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QTableWidgetItem:
    if widget is None:
        widget = QTableWidgetItem()

    set_widget_text(widget, text)
    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    return widget


def TreeWidget(
    *,
    widget: Optional[QTreeWidget] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QTreeWidget:
    if widget is None:
        widget = QTreeWidget()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    return widget


def TreeWidgetItem(
    *,
    widget: Optional[QTableWidgetItem] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QTreeWidgetItem:
    if widget is None:
        widget = QTreeWidgetItem()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    return widget


# Icons


def PixmapM(
    image_name: str,
    *,
    image_size: Optional[Tuple[int, int]] = None,
    color: Optional[Tuple[int, int, int, int]] = None,
):
    image_path: Optional[str] = None
    if image_name.startswith("ma-"):
        image_path = f":/material-icons/{image_name}.png"
    elif image_name.startswith("i8-"):
        image_path = f":/icons8-icons/{image_name}.svg"

    if image_path is None:
        return None

    pixmap = QPixmap(image_path)

    if color is not None:
        if isinstance(color, tuple):
            color = QColor(color[0], color[1], color[2], color[3])

        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        del painter

    if isinstance(image_size, tuple):
        pixmap = pixmap.scaled(
            QSize(image_size[0], image_size[1]),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    return pixmap


def IconM(
    icon_name: str,
    *,
    icon_size: Optional[Tuple[int, int]] = None,
    color: Optional[Union[Tuple[int, int, int, int], QColor]] = None,
) -> QIcon:
    """Load icons from resources.
    Material Design icons starts with "ma-", "ma-add-black.png"
    Icons8 (flat icons) starts with "i8-", "i8-callendar"

    Args:
        icon_name (str):
        icon_size (Optional[Tuple[int, int]]):
        color (Optional[Union[Tuple[int, int, int, int], QColor]]):
    Returns:
        QIcon: out
    """
    icon_path: Optional[str] = None
    if icon_name.startswith("ma-"):
        icon_path = f":/material-icons/{icon_name}.png"
    elif icon_name.startswith("i8-"):
        icon_path = f":/icons8-icons/{icon_name}.svg"

    if icon_path is None:
        return None

    pixmap = QPixmap(icon_path)

    if color is not None:
        if isinstance(color, tuple):
            color = QColor(color[0], color[1], color[2], color[3])

        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        del painter

    if isinstance(icon_size, tuple):
        pixmap = pixmap.scaled(
            QSize(icon_size[0], icon_size[1]),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
    return QIcon(pixmap)


# Action


def Action(
    text: Optional[str] = None,
    *,
    icon: Optional[QIcon] = None,
    triggered: Optional[Slot] = None,
    shortcut: Optional[
        Union[
            QKeySequence,
            QKeyCombination,
            QKeySequence.StandardKey,
            str,
            int,
        ]
    ] = None,
    parent: Optional[QObject] = None,
) -> QAction:
    action = QAction(text, parent=parent)

    if shortcut is not None:
        action.setShortcut(shortcut)

    if icon is not None:
        action.setIcon(icon)

    if triggered:
        action.triggered.connect(triggered)

    return action


# Menu


def Menu(
    title: str,
    *,
    items: Optional[List[Union[QMenu, QAction, str]]] = None,
    css: Optional[str] = None,
) -> QMenu:
    menu = QMenu(title)

    set_widget_style_sheet(menu, css)

    if isinstance(items, list):
        for item in items:
            if isinstance(item, str):
                if item == "separator":
                    menu.addSeparator()
            elif isinstance(item, QMenu):
                menu.addMenu(item)
            elif isinstance(item, QAction):
                menu.addAction(item)

    return menu


def MenuBar(
    *menus,
    css: Optional[str] = None,
) -> QMenuBar:
    menubar = QMenuBar()

    set_widget_style_sheet(menubar, css)

    for menu in menus:
        menubar.addMenu(menu)

    return menubar


# Tool Bar


class ToolBarNextLine:
    pass


def ToolBar(
    title: Optional[str] = None,
    items: Optional[List[Union[QAction, QMenu]]] = None,
) -> QToolBar:
    toolbar = QToolBar(title)

    if items:
        for item in items:
            if isinstance(item, QAction):
                toolbar.addAction(item)
            elif isinstance(item, QWidget):
                toolbar.addWidget(item)

    return toolbar


# Status Bar


def StatusBar() -> QStatusBar:
    statusbar = QStatusBar()

    return statusbar


def DockWidget(
    title: Optional[str] = None,
    widget: Optional[QWidget] = None,
    *,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QDockWidget:
    dock: QDockWidget = QDockWidget()

    set_widget_object_name(dock, object_name)
    set_widget_style_sheet(dock, css)
    size_ops_set(dock, size_ops)

    if title is not None:
        dock.setWindowTitle(title)

    if widget is not None:
        dock.setWidget(widget)

    return dock


class DockWidgetSized(QDockWidget):
    def __init__(
        self,
        *,
        widget: Optional[QWidget] = None,
        size_hint: Tuple[int, int],
        title: str,
    ) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setWidget(widget)
        self._size_hint = size_hint

    def set_hint_size(self, w: int, h: int) -> None:
        self._hint_width = w
        self._hint_height = h

    def sizeHint(self) -> QSize:
        return QSize(self._hint_width, self._hint_height)

    def minimumSizeHint(self) -> QSize:
        return QSize(self._hint_width, self._hint_height)


# Layouts


def Splitter(
    widgets: Optional[List[QWidget]] = None,
    *,
    sizes: Optional[Sequence[int]] = None,
    splitter: Optional[QSplitter] = None,
    orientation: Optional[Qt.Orientation] = Qt.Orientation.Horizontal,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
    margin: Optional[int] = None,
) -> QSplitter:
    if splitter is None:
        splitter = QSplitter()

    set_widget_object_name(splitter, object_name)
    set_widget_style_sheet(splitter, css)
    size_ops_set(splitter, size_ops)

    if margin is not None:
        splitter.setContentsMargins(margin, margin, margin, margin)

    if orientation is not None:
        splitter.setOrientation(orientation)

    if widgets is not None:
        for widget in widgets:
            splitter.addWidget(widget)

    if sizes is not None:
        splitter.setSizes(sizes)

    return splitter


def SpacerItem(
    *,
    width: Optional[int] = None,
    height: Optional[int] = None,
    horizontal_policy: Optional[int] = SizePolicy.Expanding,
    vertical_policy: Optional[int] = SizePolicy.Expanding,
    widget: Optional[QSpacerItem] = None,
) -> None:
    widget = QSpacerItem(width, height, horizontal_policy, vertical_policy)

    return widget


def VSpacer() -> QSpacerItem:
    return SpacerItem(
        width=1,
        height=1,
        horizontal_policy=SizePolicy.Minimum,
        vertical_policy=SizePolicy.Expanding,
    )


def HSpacer() -> QSpacerItem:
    return SpacerItem(
        width=1,
        height=1,
        horizontal_policy=SizePolicy.Expanding,
        vertical_policy=SizePolicy.Minimum,
    )


def ScrollArea(
    *,
    scroll_area: Optional[QScrollArea] = None,
    parent: Optional[QWidget] = None,
    widget: Optional[QWidget] = None,
    object_name: Optional[str] = None,
    css: Optional[str] = None,
    resizable: Optional[bool] = True,
) -> QScrollArea:
    if scroll_area is None:
        scroll_area = QScrollArea(parent)

    set_widget_object_name(scroll_area, object_name)
    set_widget_style_sheet(scroll_area, css)

    if widget is not None:
        scroll_area.setWidget(widget)

    if resizable is not None:
        scroll_area.setWidgetResizable(resizable)

    return scroll_area


class Align:
    Top: Final = Qt.AlignmentFlag.AlignTop
    Bottom: Final = Qt.AlignmentFlag.AlignBottom
    Left: Final = Qt.AlignmentFlag.AlignLeft
    Right: Final = Qt.AlignmentFlag.AlignRight
    Center: Final = Qt.AlignmentFlag.AlignCenter
    VCenter: Final = Qt.AlignmentFlag.AlignVCenter


def _set_layout_props(
    layout: QLayout,
    align: Optional[int] = None,
    spacing: Optional[int] = None,
    margin: Optional[int] = None,
) -> None:
    if align is not None:
        layout.setAlignment(align)
    if spacing is not None:
        layout.setSpacing(spacing)
    if margin is not None:
        layout.setContentsMargins(margin, margin, margin, margin)


def VBox(
    *items,
    align: Optional[int] = Align.Top,
    spacing: Optional[int] = None,
    margin: Optional[int] = None,
    stretch_factor: Optional[int] = 0,
) -> QVBoxLayout:
    box = QVBoxLayout()
    _set_layout_props(box, align, spacing, margin)
    for item in items:
        stretch = stretch_factor
        if isinstance(item, (tuple, list)):
            assert len(item) == 2
            stretch = item[1]
            item = item[0]

        if isinstance(item, QWidget):
            box.addWidget(item, stretch)
        elif isinstance(item, QLayout):
            box.addLayout(item, stretch)
        else:
            print("Error adding item: type is not acceptable", item)
    return box


def HBox(
    *items,
    align: Optional[int] = Align.Top,
    spacing: Optional[int] = None,
    margin: Optional[int] = None,
    stretch_factor: Optional[int] = 0,
) -> QHBoxLayout:
    box = QHBoxLayout()
    _set_layout_props(box, align, spacing, margin)
    for item in items:
        stretch = stretch_factor
        if isinstance(item, (tuple, list)):
            assert len(item) == 2
            stretch = item[1]
            item = item[0]

        if isinstance(item, QWidget):
            box.addWidget(item, stretch)
        elif isinstance(item, QLayout):
            box.addLayout(item, stretch)
        else:
            print("Error adding item: type is not acceptable", item)
    return box


class NextColumn:
    pass


class NextRow:
    pass


class AddStretch:
    pass


class AddStretchLayout:
    pass


def Columns(
    *items,
    align: Optional[int] = None,
    spacing: Optional[int] = None,
    margin: Optional[int] = None,
    stretch_factor: int = 0,
) -> QHBoxLayout:
    box = QHBoxLayout()
    _set_layout_props(box, align, spacing, margin)

    init_layout = True
    layout_item = None
    for item in items:
        stretch = stretch_factor

        if isinstance(item, (tuple, list)):
            assert len(item) == 2, "Item"
            stretch = item[1]
            item = item[0]
        if item == NextColumn or init_layout:
            init_layout = False
            layout_item = QVBoxLayout()
            _set_layout_props(layout_item, align, spacing, margin)
            box.addLayout(layout_item, stretch)

        if isinstance(item, QWidget):
            layout_item.addWidget(item, stretch)
        elif isinstance(item, QLayout):
            layout_item.addLayout(item, stretch)
        elif isinstance(item, QSpacerItem):
            layout_item.addItem(item)

        elif item == AddStretch:
            layout_item.addStretch()
        elif item == AddStretchLayout:
            box.addStretch()

    return box


def Rows(
    *items,
    align: Optional[int] = None,
    spacing: Optional[int] = None,
    margin: Optional[int] = None,
    stretch_factor: int = 0,
) -> QVBoxLayout:
    box = QVBoxLayout()
    _set_layout_props(box, align, spacing, margin)
    init_layout = True
    layout_item = None
    for item in items:
        stretch = stretch_factor

        if isinstance(item, (tuple, list)):
            assert len(item) == 2, "Item"
            stretch = item[1]
            item = item[0]
        if item == NextRow or init_layout:
            init_layout = False
            layout_item = QHBoxLayout()
            _set_layout_props(layout_item, align, spacing, margin)
            box.addLayout(layout_item, stretch)

        if isinstance(item, QWidget):
            layout_item.addWidget(item, stretch)
        elif isinstance(item, QLayout):
            layout_item.addLayout(item, stretch)
        elif isinstance(item, QSpacerItem):
            layout_item.addItem(item)

        elif item == AddStretch:
            layout_item.addStretch()
        elif item == AddStretchLayout:
            box.addStretch()

    return box


def set_uniform_label_width(form_layout):
    max_width = 0

    # Iterate over all rows in the form layout
    for i in range(form_layout.rowCount()):
        widget = form_layout.itemAt(i, QFormLayout.LabelRole).widget()

        # Check if the widget is a QLabel
        if isinstance(widget, QLabel):
            max_width = max(max_width, widget.sizeHint().width())
    max_width = int(max_width * 1.1)
    # Set the maximum width to all QLabel widgets
    for i in range(form_layout.rowCount()):
        widget = form_layout.itemAt(i, QFormLayout.LabelRole).widget()
        if isinstance(widget, QLabel):
            widget.setFixedWidth(max_width)


def Form(
    *items: List[Tuple[Union[str, QLabel], QWidget]],
    align: Optional[int] = None,
    spacing: Optional[int] = None,
    margin: Optional[int] = None,
    label_align: int = Align.Right,
    uniform_label_width: bool = True,
) -> QFormLayout:
    box = QFormLayout()
    _set_layout_props(box, align, spacing, margin)

    for text, item in items:
        if isinstance(text, str):
            label = Label(text)
        if isinstance(text, QLabel):
            label.setAlignment(label_align)
        box.addRow(label, item)

    box.setLabelAlignment(label_align)
    if uniform_label_width:
        set_uniform_label_width(box)
    return box


def GroupBox(
    title: str,
    *,
    widget: Optional[QGroupBox] = None,
    layout: Optional[QGroupBox] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QGroupBox:
    if widget is None:
        widget = QGroupBox(title)
    widget.setTitle(title)

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if layout is not None:
        widget.setLayout(layout)

    return widget


# Frame


def Frame(
    *,
    widget: Optional[QFrame] = None,
    layout: Optional[QLayout] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QFrame:
    if widget is None:
        widget = QFrame()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if layout is not None:
        widget.setLayout(layout)

    return widget


def HLine() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)

    line.setFrameShadow(QFrame.Shadow.Sunken)
    line.setFixedHeight(2)
    line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    return line


# Stacked Widget


def StackedWidget(
    *,
    widget: Optional[QStackedWidget] = None,
    layout: Optional[QLayout] = None,
    pages: Optional[List[QWidget]] = None,
    current_page_index: Optional[int] = None,
    current_page: Optional[QWidget] = None,
    object_name: Optional[str] = None,
    size_ops: Optional[SizeOps] = None,
    css: Optional[str] = None,
) -> QStackedWidget:
    if widget is None:
        widget = QStackedWidget()

    set_widget_object_name(widget, object_name)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if layout is not None:
        widget.setLayout(layout)

    if pages is not None:
        for page in pages:
            widget.addWidget(page)

    if current_page_index is not None:
        widget.setCurrentIndex(current_page_index)
    elif current_page is not None:
        widget.setCurrentWidget(current_page)

    return widget


# Window


def Widget(
    *,
    widget: Optional[QWidget] = None,
    layout: Optional[QLayout] = None,
    object_name: Optional[str] = None,
    window_ops: Optional[WindowOps] = None,
    size_ops: Optional[SizeOps] = None,
    show: bool = False,
    css: Optional[str] = None,
) -> QWidget:
    if widget is None:
        widget = QWidget()

    if layout is not None:
        widget.setLayout(layout)

    set_widget_object_name(widget, object_name)
    window_ops_set(widget, window_ops)
    set_widget_style_sheet(widget, css)
    size_ops_set(widget, size_ops)

    if show:
        widget.show()

    return widget


def MainWindow(
    *,
    widget: Optional[QMainWindow] = None,
    window_ops: Optional[WindowOps] = None,
    central_widget: Optional[QWidget] = None,
    docks: Optional[List[Tuple[int, QDockWidget]]] = None,
    menubar: Optional[QMenuBar] = None,
    toolbars: Optional[List[QToolBar]] = None,
    statusbar: Optional[QStatusBar] = None,
    css: Optional[str] = None,
    show: bool = False,
) -> QMainWindow:
    if widget is None:
        widget = QMainWindow()

    window_ops_set(widget, window_ops)
    set_widget_style_sheet(widget, css)

    if isinstance(central_widget, QWidget):
        widget.setCentralWidget(central_widget)

    if docks is not None:
        for area, dock in docks:
            widget.addDockWidget(area, dock)

    if menubar is not None:
        widget.setMenuBar(menubar)

    if toolbars is not None:
        for toolbar in toolbars:
            if toolbar == ToolBarNextLine:
                widget.addToolBarBreak()
            else:
                widget.addToolBar(toolbar)

    if statusbar is not None:
        widget.setStatusBar(statusbar)

    if show:
        widget.show()

    return widget


# Dialogs


def Alert(
    title: str,
    message: str,
    parent: Optional[QWidget] = None,
) -> None:
    print(title, message, parent)
    QMessageBox.warning(parent, title, message, QMessageBox.StandardButton.Ok)


def Error(
    title: str,
    message: str,
    parent: Optional[QWidget] = None,
    msg_type: Optional[str] = None,
    modal: bool = False,
) -> QErrorMessage:
    err = QErrorMessage(parent)
    err.setWindowTitle(title)
    err.setModal(modal)
    err.showMessage(message, msg_type)
    return err


def Confirm(
    title: str,
    message: str,
    parent: Optional[QWidget] = None,
) -> bool:
    reply = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.Yes | QMessageBox.Cancel,
    )
    return reply == QMessageBox.Yes


def Color(
    title: str = None,
    color: Union[Tuple[int, int, int], Tuple[int, int, int, int], QColor] = (
        77,
        77,
        77,
    ),
    parent: Optional[QWidget] = None,
) -> QColor | None:
    initial: QColor | None = None
    if isinstance(color, QColor):
        initial = color
    elif isinstance(color, tuple):
        for c in color:
            assert isinstance(c, int) and 0 <= c <= 255
        if len(color) == 4:
            initial = QColor(color[0], color[1], color[2], color[3])
        else:
            initial = QColor(color[0], color[1], color[2])

    color = QColorDialog.getColor(
        initial,
        parent,
        title,
        QColorDialog.ShowAlphaChannel,
        # | QColorDialog.NoButtons | QColorDialog.DontUseNativeDialog
    )
    if color.isValid():
        return color
    return initial


def OpenFile(
    title: Optional[str] = "Open File...",
    file_filter: Optional[str] = "All Files(*);;Text Files (*.txt)",
    directory: Optional[str] = None,
    parent: Optional[QWidget] = None,
    native: bool = True,
) -> Optional[str]:
    options = QFileDialog.Option()
    if not native:
        options = QFileDialog.Option.DontUseNativeDialog

    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        title,
        directory,
        file_filter,
        options=options,
    )

    if file_path:
        return file_path.replace(os.sep, "/")

    return None


def OpenFiles(
    title: Optional[str] = "Open File...",
    file_filter: Optional[str] = "All Files(*);;Text Files (*.txt)",
    directory: Optional[str] = None,
    parent: Optional[QWidget] = None,
    native: bool = True,
) -> List[str] | None:
    options = QFileDialog.Option()
    if not native:
        options = QFileDialog.Option.DontUseNativeDialog

    files, _ = QFileDialog.getOpenFileNames(
        parent,
        title,
        directory,
        file_filter,
        options=options,
    )

    output: List[str] = list()
    if files:
        for file_path in files:
            output.append(file_path.replace(os.sep, "/"))
        return sorted(output)
    return output


def SaveFile(
    title: Optional[str] = "Open File...",
    directory: Optional[str] = None,
    file_filter: Optional[str] = "All Files(*);;Text Files (*.txt)",
    parent: Optional[QWidget] = None,
    native: bool = True,
) -> Optional[str]:
    options = QFileDialog.Option()
    if not native:
        options = QFileDialog.Option.DontUseNativeDialog

    file_path, _ = QFileDialog.getSaveFileName(
        parent,
        title,
        directory,
        file_filter,
        options=options,
    )

    if file_path:
        return file_path.replace(os.sep, "/")

    return None


def OpenDir(
    title: Optional[str] = "Open Directory...",
    directory: Optional[str] = None,
    parent: Optional[QWidget] = None,
    show_dirs_only: bool = True,
    native: bool = True,
) -> Optional[str]:
    options = QFileDialog.Option()
    if not native:
        options = QFileDialog.Option.DontUseNativeDialog
    if show_dirs_only:
        options |= QFileDialog.Option.ShowDirsOnly
    else:
        options &= ~QFileDialog.Option.ShowDirsOnly

    dir_path = QFileDialog().getExistingDirectory(
        parent, caption=title, dir=directory, options=options
    )

    if dir_path:
        return dir_path.replace(os.sep, "/")

    return None


# Application


class ApplicationContext:
    """A context object to be shared through different threads and application
    layers to avoid use of global.

    Common utilities:
        Logging, Event Manager reference, settings

    Recommendations:
        For a GUI application, it can be used as a base class to handle events,
        settings, and logging.

    """

    def __init__(self, name: str = "[MAIN]") -> None:
        self.data = dict(
            name=name,
            event_manager=None,
            settings=None,
            log=None,
        )

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value) -> None:
        self.data[key] = value

    @property
    def name(self) -> str:
        return self.data["name"]


def Application(
    ctx: ApplicationContext,
    argv: Optional[List[str]] = None,
    css: Optional[str] = None,
) -> QApplication:
    app = QApplication(argv)
    app.ctx = ctx
    if css is not None:
        app.setStyleSheet(css)
    return app


def app_set_font(
    app: QApplication,
    font_path: str = ":/fonts/roboto/Roboto-Regular.ttf",
    font_size: int = 14,
) -> None:
    font_id = QFontDatabase.addApplicationFont(font_path)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    font = QFont(font_family)
    font.setPixelSize(font_size)
    app.setFont(font)


# timer
def Timer(
    *,
    interval_ms: int = 1000,
    single_shot: bool = False,
    on_timeout: Optional[Slot] = None,
    auto_start: bool = False,
) -> QtCore.QTimer:
    timer = QtCore.QTimer()
    timer.setInterval(interval_ms)
    timer.setSingleShot(single_shot)
    timer.timeout.connect(on_timeout)
    if auto_start:
        timer.start()

    return timer

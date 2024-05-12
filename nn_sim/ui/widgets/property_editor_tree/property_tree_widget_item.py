#
# Author: Joed Lopes da Silva
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


import os
from typing import Union, List, Optional, Dict, Any

from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtGui import QIcon, QPixmap, QImage
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QWidget,
    QTreeWidgetItem,
    QTreeWidget,
    QItemDelegate,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QAbstractItemDelegate,
    QStyleOptionViewItem,
    QStyledItemDelegate,
)

from .property_model import (
    PropertyGroupModel,
    PropertyItemModel,
    PropertyTypes,
    EditorOptions,
    get_dict_value,
)
from .editor_factory import EditorFactory


class NoEditableDelegate(QStyledItemDelegate):
    def __init__(self, parent=None) -> None:
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        return None


class PropertyItemDelegate(QItemDelegate):
    def __init__(self, parent) -> None:
        QItemDelegate.__init__(self, parent)
        self.closeEditor.connect(self.__on_close_editor)
        self.property_item_model: Optional["PropertyItemModel"] = None

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> Optional[QWidget]:
        if index.column() != 1:
            return None

        item = parent.parent().currentItem()
        self.property_item_model = item.property_item_model
        assert isinstance(self.property_item_model, PropertyItemModel)

        if self.property_item_model.is_editable() is False:
            return None

        self.editor = EditorFactory.create_tree_item_editor(
            parent, self.property_item_model
        )

        # register item changed
        if isinstance(self.editor, QLineEdit):
            pass
        elif isinstance(self.editor, QComboBox):
            self.editor.currentIndexChanged.connect(self.on_editor_changed)
        elif isinstance(self.editor, QSpinBox):
            self.editor.valueChanged.connect(self.on_editor_changed)
        elif isinstance(self.editor, QDoubleSpinBox):
            self.editor.valueChanged.connect(self.on_editor_changed)

        return self.editor

    def on_editor_changed(self, arg1=None):
        PropertyItemDelegate.editor_changed(
            self.editor, self.property_item_model, False
        )

    def __on_close_editor(
        self, editor_widget: "QWidget", hint: QAbstractItemDelegate.EndEditHint
    ) -> None:
        PropertyItemDelegate.editor_changed(
            editor_widget, self.property_item_model, True
        )

    @staticmethod
    def editor_changed(
        editor_widget: QWidget,
        property_item_model: "PropertyItemModel",
        trigger=True,
    ) -> None:
        if isinstance(editor_widget, QLineEdit):
            if property_item_model.get_type() == PropertyTypes.TEXT:
                value = editor_widget.text()
                property_item_model.set_value(value, trigger_specific_event=trigger)

        elif isinstance(editor_widget, QComboBox):
            if property_item_model.get_type() == PropertyTypes.BOOLEAN:
                bool_value = True if editor_widget.currentIndex() > 0 else False
                property_item_model.set_value(
                    bool_value, trigger_specific_event=trigger
                )

            elif property_item_model.get_type() == PropertyTypes.TEXT:
                current_text = editor_widget.currentText()

                options: dict = property_item_model.get_editor_options()
                item_options: List[str] = options[EditorOptions.COMBO_BOX_OPTIONS]

                if current_text in item_options:
                    property_item_model.set_value(
                        current_text, trigger_specific_event=trigger
                    )
                else:
                    print("WARNING", "combobox item option is invalid:", current_text)

        elif isinstance(editor_widget, QSpinBox):
            int_value = editor_widget.value()
            property_item_model.set_value(int_value, trigger_specific_event=trigger)

        elif isinstance(editor_widget, QDoubleSpinBox):
            real_value = editor_widget.value()
            if real_value != property_item_model.get_value():
                property_item_model.set_value(
                    real_value, trigger_specific_event=trigger
                )


class ItemIcons:
    FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

    @staticmethod
    def get(icon_name: str) -> QIcon:
        return QIcon(os.path.join(ItemIcons.FOLDER_PATH, icon_name + ".png"))

    @staticmethod
    def create_label_icon(icon_name, width=20, tooltip=""):
        label = QLabel()
        icon_path = os.path.join(ItemIcons.FOLDER_PATH, icon_name + ".png")
        label.setStyleSheet("background: transparent;")
        label.setPixmap(QPixmap(QImage(icon_path)))
        label.setCursor(Qt.PointingHandCursor)
        label.setFixedWidth(width)
        label.setToolTip(tooltip)
        return label


class PropertyTreeItemWidget(QTreeWidgetItem):
    def __init__(
        self,
        parent_tree: "QTreeWidget",
        property_group_tree_item: "PropertyGroupTreeItemWidget",
        property_item_model: "PropertyItemModel",
    ) -> None:
        assert isinstance(property_item_model, PropertyItemModel)

        QTreeWidgetItem.__init__(self, property_group_tree_item)

        self.parent_tree: QTreeWidget = parent_tree
        self.property_group_tree_item: "PropertyGroupTreeItemWidget" = (
            property_group_tree_item
        )
        self.property_item_model: PropertyItemModel = property_item_model
        self.property_item_model.set_specific_listener(self)

        self.check_box_items: Union[dict, None] = None

        self.parent_tree.setItemWidget(
            self, 2, ItemIcons.create_label_icon("edit", 16, "Edit Item")
        )
        self.parent_tree.setItemWidget(
            self, 3, ItemIcons.create_label_icon("delete", 16, "Delete Item")
        )

        self.update_item()

    def on_property_item_changed(
        self, property_item_model: "PropertyItemModel"
    ) -> None:
        if self.property_item_model == property_item_model:
            # print('on_property_item_changed')
            self.update_item()

    def update_item(self):
        if self.property_item_model.is_editable():
            self.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.setDisabled(False)
        else:
            self.setDisabled(True)

        self.setText(0, self.property_item_model.get_name())

        options: Dict[str, Any] = self.property_item_model.get_editor_options()

        if self.property_item_model.get_type() == PropertyTypes.BOOLEAN:
            self.setText(
                1, EditorFactory.get_boolean_value_as_text(self.property_item_model)
            )
            return

        elif get_dict_value(options, EditorOptions.CHECK_BOX, bool, False) is True:
            if self.check_box_items is None:
                self.__create_checkbox_items()

        # print('UPDATE ITEM - %s' % str(self.property_item_model.get_value()))

        value = self.property_item_model.get_value()
        if value is not None:
            value = str(value)
        else:
            value = ""

        self.setText(1, value)

    def __create_checkbox_items(self):
        options: Dict[str, Any] = self.property_item_model.get_editor_options()
        item_options: List[str] = options[EditorOptions.CHECK_BOX_OPTIONS]

        values: Optional[str] = self.property_item_model.get_value()
        if values is None:
            values = list()

        self.check_box_items = list()

        for item in item_options:
            check = QCheckBox(item)
            # check.setStyleSheet("background: transparent;")
            check.setLayoutDirection(Qt.LeftToRight)
            is_checked = item in values
            check.setChecked(is_checked)
            check.stateChanged.connect(self._on_check_box_item_changed)

            tree_item = QTreeWidgetItem()

            self.addChild(tree_item)
            self.parent_tree.setItemWidget(tree_item, 0, check)
            tree_item.setFirstColumnSpanned(True)
            self.check_box_items.append(check)

    def _on_check_box_item_changed(self):
        value: List[str] = list()
        for check in self.check_box_items:
            assert isinstance(check, QCheckBox)
            if check.isChecked():
                value.append(check.text())
        self.property_item_model.set_value(value)

    def item_delete(self):
        print("item delete")
        # open delete editor

    def item_open_editor(self):
        # print('item open editor')

        options: Dict[str, Any] = self.property_item_model.get_editor_options()

        if get_dict_value(options, EditorOptions.SAVE_FILE_PATH_EDITOR, bool, False):
            file_filter = get_dict_value(
                options, EditorOptions.FILE_PATH_FILTER, str, None
            )
            file_filter = "All Files (*.*)"

            file_path = QFileDialog.getOpenFileName(
                None,
                "Open %s file" % self.property_item_model.get_name(),
                filter=file_filter,
            )
            if file_path:
                self.property_item_model.set_value(file_path[0])

        elif get_dict_value(options, EditorOptions.OPEN_FILE_PATH_EDITOR, bool, False):
            file_filter = get_dict_value(
                options, EditorOptions.FILE_PATH_FILTER, str, None
            )
            if file_filter is None:
                file_filter = "All Files (*.*)"

            file_path = QFileDialog.getSaveFileName(
                None,
                "Open %s file" % self.property_item_model.get_name(),
                filter=file_filter,
            )
            if file_path:
                self.property_item_model.set_value(file_path[0])

        elif get_dict_value(options, EditorOptions.FOLDER_PATH_EDITOR, bool, False):
            folder_path = QFileDialog.getExistingDirectory(
                None, "Open %s file" % self.property_item_model.get_name()
            )
            if folder_path:
                self.property_item_model.set_value(folder_path)

        else:
            self.parent_tree.editItem(self, 1)

        # open editor widget


class PropertyGroupTreeItemWidget(QTreeWidgetItem):
    def __init__(
        self,
        parent_tree: Union[QTreeWidget, "PropertyGroupTreeItemWidget"],
        property_group_model: "PropertyGroupModel",
    ) -> None:
        QTreeWidgetItem.__init__(self, parent_tree)

        assert isinstance(property_group_model, PropertyGroupModel)
        self.property_group_model: Optional["PropertyGroupModel"] = property_group_model
        self.parent_tree: Union[
            QTreeWidget, "PropertyGroupTreeItemWidget"
        ] = parent_tree

        self.setText(0, self.property_group_model.get_name())
        self.setFirstColumnSpanned(True)

        items = self.property_group_model.get_items()
        for item in items:
            tree_item: Optional[
                Union["PropertyGroupTreeItemWidget", PropertyTreeItemWidget]
            ] = None
            if isinstance(item, PropertyGroupModel):
                tree_item = PropertyGroupTreeItemWidget(self, item)
            elif isinstance(item, PropertyItemModel):
                tree_item = PropertyTreeItemWidget(self.parent_tree, self, item)
            else:
                raise Exception("Invalid type")

            self.addChild(tree_item)

#
# Author: Joed Lopes da Silva
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

__version__ = 0.1


from typing import Optional, List


from PySide6.QtWidgets import (
    QTreeWidget,
    QHeaderView,
    # QAbstractItemView
)

from .property_model import (
    PropertyModel,
    PropertyGroupModel,
    # PropertyItemModel, PropertyModelListener
)

from .property_tree_widget_item import (
    PropertyGroupTreeItemWidget,
    PropertyTreeItemWidget,
    PropertyItemDelegate,
    NoEditableDelegate,
)


class PropertyTreeWidget(QTreeWidget):
    def __init__(self, property_model: Optional[PropertyModel] = None) -> None:
        QTreeWidget.__init__(self)

        assert isinstance(property_model, PropertyModel) or property_model is None
        self.property_model = property_model

        self.setColumnCount(4)

        self.setHeaderLabels(["Property", "Value", "", ""])
        self.setWordWrap(True)
        self.setRootIsDecorated(False)
        self.setDropIndicatorShown(False)

        for col in [0, 2, 3]:
            self.setItemDelegateForColumn(col, NoEditableDelegate(self))
        self.setItemDelegateForColumn(1, PropertyItemDelegate(self))

        # self.setEditTriggers(QAbstractItemView.EditKeyPressed |
        #                     QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.itemClicked.connect(self.on_item_clicked)

        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.Fixed)
        self.header().setSectionResizeMode(3, QHeaderView.Fixed)

        self.header().setMinimumSectionSize(1)

        self.update_view()

    def set_property_model(
        self, property_model: Optional[PropertyModel] = None
    ) -> None:
        assert isinstance(property_model, PropertyModel) or property_model is None
        self.property_model = property_model
        self.update_view()

    def update_view(self) -> None:
        while self.topLevelItemCount() > 0:
            self.takeTopLevelItem(0)

        if isinstance(self.property_model, PropertyModel):
            items: List[PropertyGroupModel] = self.property_model.get_items()
            for item_model in items:
                # print('update view', item_model)
                tree_item: PropertyGroupTreeItemWidget = PropertyGroupTreeItemWidget(
                    self, item_model
                )
                self.addTopLevelItem(tree_item)
                tree_item.setExpanded(True)

        self.resizeColumnToContents(0)
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(3)

    def update_values(self, values) -> None:
        if isinstance(self.property_model, PropertyModel):
            self.property_model.update_values(values)

    def on_item_clicked(self, item, column) -> None:
        if isinstance(item, PropertyTreeItemWidget):
            if column == 2:
                item.item_open_editor()
            elif column == 3:
                item.item_delete()

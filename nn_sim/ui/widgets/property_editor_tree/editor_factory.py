#
# Author: Joed Lopes da Silva
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


from typing import Union, List, Optional


from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
)

from .property_model import (
    PropertyItemModel,
    PropertyTypes,
    EditorOptions,
    get_dict_value,
)


class EditorFactory:
    @staticmethod
    def create_tree_item_editor(
        parent: QWidget,
        property_item_model: PropertyItemModel,
    ) -> Optional[QWidget]:
        assert isinstance(property_item_model, PropertyItemModel)

        item_type: str = property_item_model.get_type()
        is_array: bool = property_item_model.is_array()

        options: dict = property_item_model.get_editor_options()

        if is_array is True:
            return None

        if item_type == PropertyTypes.TEXT:
            for key in [
                EditorOptions.CHECK_BOX,
                EditorOptions.TEXT_MULTILINE_EDITOR,
                EditorOptions.OPEN_FILE_PATH_EDITOR,
                EditorOptions.SAVE_FILE_PATH_EDITOR,
                EditorOptions.FOLDER_PATH_EDITOR,
            ]:
                if get_dict_value(options, key, bool, False):
                    return None  # implemented outside

            if get_dict_value(options, EditorOptions.COMBO_BOX, bool, False):
                return EditorFactory.create_combobox(parent, property_item_model)

            return EditorFactory.create_text_line_edit(parent, property_item_model)

        if item_type == PropertyTypes.BOOLEAN:
            return EditorFactory.create_boolean(parent, property_item_model)

        if item_type == PropertyTypes.INTEGER:
            return EditorFactory.create_integer_spin(parent, property_item_model)

        if item_type == PropertyTypes.REAL_NUMBER:
            return EditorFactory.create_real_number_spin(parent, property_item_model)

        return None

    @staticmethod
    def create_real_number_spin(
        parent: Union[QWidget, None],
        property_item_model: PropertyItemModel,
    ) -> QDoubleSpinBox:
        editor = QDoubleSpinBox(parent)

        options: dict = property_item_model.get_editor_options()

        min_value = get_dict_value(
            options, EditorOptions.NUMBER_MININUM_VALUE, float, None
        )
        max_value = get_dict_value(
            options, EditorOptions.NUMBER_MAXIMUM_VALUE, float, None
        )
        step_value = get_dict_value(
            options, EditorOptions.NUMBER_STEP_VALUE, float, None
        )
        precision_value = get_dict_value(
            options, EditorOptions.NUMBER_PRECISION, int, None
        )

        if max_value is not None:
            editor.setMaximum(max_value)
        if min_value is not None:
            editor.setMinimum(min_value)
        if step_value is not None:
            editor.setSingleStep(step_value)
        if precision_value is not None:
            editor.setDecimals(precision_value)

        return editor

    @staticmethod
    def create_integer_spin(
        parent: Union[QWidget, None],
        property_item_model: PropertyItemModel,
    ) -> QSpinBox:
        editor: QSpinBox = QSpinBox(parent)

        options: dict = property_item_model.get_editor_options()

        min_value: Union[int, None] = get_dict_value(
            options, EditorOptions.NUMBER_MININUM_VALUE, int, None
        )
        max_value: Union[int, None] = get_dict_value(
            options, EditorOptions.NUMBER_MAXIMUM_VALUE, int, None
        )
        step_value: Union[int, None] = get_dict_value(
            options, EditorOptions.NUMBER_STEP_VALUE, int, None
        )

        if max_value is not None:
            editor.setMaximum(max_value)
        if min_value is not None:
            editor.setMinimum(min_value)
        if step_value is not None:
            editor.setSingleStep(step_value)

        return editor

    @staticmethod
    def create_boolean(
        parent: Union[QWidget, None],
        property_item_model: PropertyItemModel,
    ) -> QSpinBox:
        editor: QComboBox = QComboBox(parent)

        options: dict = property_item_model.get_editor_options()

        text_true: Union[str, None] = get_dict_value(
            options, EditorOptions.BOOLEAN_TRUE_TEXT, str, None
        )
        text_false: Union[str, None] = get_dict_value(
            options, EditorOptions.BOOLEAN_FALSE_TEXT, str, None
        )

        if text_true is None:
            text_true = "True"
        if text_false is None:
            text_false = "False"

        editor.addItems([text_false, text_true])

        if property_item_model.get_value() is True:
            editor.setCurrentIndex(1)

        return editor

    @staticmethod
    def create_combobox(
        parent: Union[QWidget, None],
        property_item_model: PropertyItemModel,
    ) -> QComboBox:
        editor: QComboBox = QComboBox(parent)

        options: dict = property_item_model.get_editor_options()
        item_options: List[str] = options[EditorOptions.COMBO_BOX_OPTIONS]
        editor.addItems(item_options)

        editor.setCurrentIndex(item_options.index(property_item_model.get_value()))

        return editor

    @staticmethod
    def create_text_line_edit(
        parent: Union[QWidget, None],
        property_item_model: PropertyItemModel,
    ) -> QLineEdit:
        editor: QLineEdit = QLineEdit(parent)
        options: dict = property_item_model.get_editor_options()

        max_size = get_dict_value(options, EditorOptions.TEXT_MAX_SIZE, int, None)
        editor.setMaxLength(max_size)

        return editor

    @staticmethod
    def get_boolean_value_as_text(
        property_item_model: PropertyItemModel,
    ) -> str:
        options: dict = property_item_model.get_editor_options()

        if property_item_model.get_value() is True:
            text_true: Union[str, None] = get_dict_value(
                options, EditorOptions.BOOLEAN_TRUE_TEXT, str, None
            )
            if text_true is None:
                return "True"
            return text_true

        text_false: Union[str, None] = get_dict_value(
            options, EditorOptions.BOOLEAN_FALSE_TEXT, str, None
        )
        if text_false is None:
            return "False"
        return text_false

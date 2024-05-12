#
# Author: Joed Lopes da Silva
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


from typing import Any, Optional, Tuple, List, Union, Callable, Final, Dict
import copy

# basic functions


def list_static_class_variables(class_to_list):
    items = list()
    for key in class_to_list.__dict__:
        if not key.startswith("__") and isinstance(class_to_list.__dict__[key], str):
            items.append(class_to_list.__dict__[key])
    return items


def filter_dict(
    source: Dict[str, Any],
    keys: List[str],
    out: Dict[str, Any] = None,
) -> Dict[str, Any]:
    if out is None:
        out = dict()
    for key in keys:
        # if does have the specified key,
        # it will throw an exception on purpose
        out[key] = copy.copy(source[key])
    return out


def check_dict_value(
    dict_object: Dict[str, Any],
    key: str,
    value_type: Any,
    expected_value: Any,
) -> bool:
    return (
        key in dict_object
        and isinstance(dict_object[key], value_type)
        and dict_object[key] == expected_value
    )


def get_dict_value(
    dict_object: Dict[str, Any],
    key: str,
    value_type: Any,
    default_value: Any,
) -> Any:
    if key in dict_object and dict_object[key] is not None:
        assert isinstance(dict_object[key], value_type)
        return dict_object[key]
    return default_value


# Model Definitions


class PropertyTypes:
    # Primitive
    TEXT: Final[str] = "text"
    INTEGER: Final[str] = "integer"
    REAL_NUMBER: Final[str] = "real_number"
    BOOLEAN: Final[str] = "boolean"

    # Misc format
    COLOR: Final[str] = "color"

    # Time format
    TIMESTAMP: Final[str] = "timestamp"
    DATE: Final[str] = "datetime"
    TIME: Final[str] = "time"

    # Points format
    POINT3D: Final[str] = "point3d"
    POINT2D: Final[str] = "point2d"


class BasicOptions:
    TYPE = "type"

    CAN_BE_NULL: Final[str] = "can_be_null"
    DEFAULT_VALUE: Final[str] = "default_value"

    IS_ARRAY: Final[str] = "is_array"
    ARRAY_DIMENSION: Final[str] = "array_dimension"

    GROUP: Final[str] = "group"


class EditorOptions:
    EDITABLE: Final[str] = "editable"
    SINGLE: Final[str] = "single"

    # only string is permited
    COMBO_BOX: Final[str] = "combo_box"
    COMBO_BOX_OPTIONS: Final[str] = "combo_box_options"

    # Checkbox value is a list of strig with the possible values
    CHECK_BOX: Final[str] = "check_box"
    CHECK_BOX_OPTIONS: Final[str] = "check_box_options"

    # Number Editor
    NUMBER_SLIDER_EDITOR: Final[str] = "number_slider_editor"
    NUMBER_SPINNER_EDITOR: Final[str] = "number_spinner_editor"

    NUMBER_MININUM_VALUE: Final[str] = "number_min_value"
    NUMBER_MAXIMUM_VALUE: Final[str] = "number_max_value"
    NUMBER_STEP_VALUE: Final[str] = "number_step_value"
    NUMBER_PRECISION: Final[str] = "number_precision"

    # Text Editor
    TEXT_LINE_EDITOR: Final[str] = "text_line_editor"
    TEXT_MULTILINE_EDITOR: Final[str] = "text_multiline_editor"
    TEXT_MIN_SIZE: Final[str] = "text_min_size"
    TEXT_MAX_SIZE: Final[str] = "text_max_size"

    # Extra Editors - Misc
    OPEN_FILE_PATH_EDITOR: Final[str] = "open_file_path_editor"
    SAVE_FILE_PATH_EDITOR: Final[str] = "save_file_path_editor"
    FILE_PATH_FILTER: Final[str] = "file_path_filter"
    FOLDER_PATH_EDITOR: Final[str] = "folder_path_editor"

    BOOLEAN_TRUE_TEXT: Final[str] = "boolean_true_text"
    BOOLEAN_FALSE_TEXT: Final[str] = "boolean_false_text"


# Listeners


class PropertyModelListener:
    def on_property_item_changed(
        self, property_item_model: "PropertyItemModel"
    ) -> None:
        raise NotImplementedError

    def on_message(self, message_type: str, message: str) -> None:
        raise NotImplementedError

    def on_property_model_changed(self, property_model: "PropertyModel") -> None:
        raise NotImplementedError


# Models


class PropertyItemModel:
    def __init__(self, listener: PropertyModelListener, params: dict) -> None:
        assert isinstance(listener, PropertyModelListener)
        assert isinstance(params, dict)
        assert isinstance(params["id"], str) and len(params["id"]) > 0
        assert isinstance(params["name"], str) and len(params["name"]) > 0
        assert isinstance(params["options"], dict)
        options = params["options"]

        valid_types = list_static_class_variables(PropertyTypes)

        assert options[BasicOptions.TYPE] in valid_types

        self._listener: PropertyModelListener = listener
        self._name: str = params["name"]
        self._id: str = params["id"]
        self._value: Any = copy.deepcopy(params["value"])

        # basic options
        self._type: str = "type_not_defined"
        self._can_be_null: bool = False
        self._is_array: bool = False
        self._array_dimension: Optional[Union[List, Tuple]] = None
        self._default_value: Any = None
        self.__parse_basic_options(options)

        # basic editor options
        self._editor_options: dict = dict()
        self.__parse_editor_options(options)

        self._aux_data: Any = None  # to be used outside (widget, etc)

        self._specific_listener: Optional[
            PropertyModelListener
        ] = None  # use along tree widget item

    def set_specific_listener(
        self, specific_listener: Optional[PropertyModelListener] = None
    ):
        self._specific_listener = specific_listener

    def set_aux_data(self, aux_data: Any) -> None:
        self._aux_data = aux_data

    def get_aux_data(self) -> Any:
        return self._aux_data

    def __parse_basic_options(self, options):
        self._type = options[BasicOptions.TYPE]
        self._can_be_null = check_dict_value(
            options, BasicOptions.CAN_BE_NULL, bool, True
        )
        self._is_array = check_dict_value(options, BasicOptions.IS_ARRAY, bool, True)
        self._array_dimension = None

        if self._is_array:
            if BasicOptions.ARRAY_DIMENSION in options:
                dimension = options[BasicOptions.ARRAY_DIMENSION]
                assert isinstance(dimension, list)
                if len(dimension) > 0:
                    for item in dimension:
                        assert isinstance(item, int)
                    self._array_dimension = copy.copy(dimension)

        if (
            BasicOptions.DEFAULT_VALUE in options
            and options[BasicOptions.DEFAULT_VALUE] is not None
        ):
            self._default_value = options[BasicOptions.DEFAULT_VALUE]
            if self._value is None:
                self._value = copy.deepcopy(self._default_value)

    def __parse_editor_options(self, options: Dict[str, Any]):
        self._editor_options[EditorOptions.EDITABLE] = get_dict_value(
            options, EditorOptions.EDITABLE, bool, True
        )

        self._editor_options[EditorOptions.SINGLE] = get_dict_value(
            options, EditorOptions.SINGLE, bool, False
        )

        self._editor_options[EditorOptions.COMBO_BOX] = get_dict_value(
            options, EditorOptions.COMBO_BOX, bool, False
        )

        self._editor_options[EditorOptions.CHECK_BOX] = get_dict_value(
            options, EditorOptions.CHECK_BOX, bool, False
        )

        self._editor_options[EditorOptions.NUMBER_SLIDER_EDITOR] = get_dict_value(
            options, EditorOptions.NUMBER_SLIDER_EDITOR, bool, False
        )

        self._editor_options[EditorOptions.NUMBER_SPINNER_EDITOR] = get_dict_value(
            options, EditorOptions.NUMBER_SPINNER_EDITOR, bool, False
        )

        self._editor_options[EditorOptions.TEXT_LINE_EDITOR] = get_dict_value(
            options, EditorOptions.TEXT_LINE_EDITOR, bool, False
        )

        self._editor_options[EditorOptions.TEXT_MULTILINE_EDITOR] = get_dict_value(
            options, EditorOptions.TEXT_MULTILINE_EDITOR, bool, False
        )

        self._editor_options[EditorOptions.BOOLEAN_TRUE_TEXT] = get_dict_value(
            options, EditorOptions.BOOLEAN_TRUE_TEXT, str, None
        )

        self._editor_options[EditorOptions.BOOLEAN_FALSE_TEXT] = get_dict_value(
            options, EditorOptions.BOOLEAN_FALSE_TEXT, str, None
        )

        self._editor_options[EditorOptions.OPEN_FILE_PATH_EDITOR] = get_dict_value(
            options, EditorOptions.OPEN_FILE_PATH_EDITOR, bool, False
        )

        self._editor_options[EditorOptions.SAVE_FILE_PATH_EDITOR] = get_dict_value(
            options, EditorOptions.SAVE_FILE_PATH_EDITOR, bool, None
        )

        self._editor_options[EditorOptions.FILE_PATH_FILTER] = get_dict_value(
            options, EditorOptions.FILE_PATH_FILTER, str, None
        )

        self._editor_options[EditorOptions.FOLDER_PATH_EDITOR] = get_dict_value(
            options, EditorOptions.FOLDER_PATH_EDITOR, bool, None
        )

        if self._editor_options[EditorOptions.CHECK_BOX] is True:
            assert self.get_type() == PropertyTypes.TEXT

            item_options = options[EditorOptions.CHECK_BOX_OPTIONS]
            assert isinstance(item_options, list) and len(item_options) > 0
            for item in item_options:
                assert isinstance(item, str) and len(item) > 0
            self._editor_options[EditorOptions.CHECK_BOX_OPTIONS] = copy.copy(
                item_options
            )

        elif self._editor_options[EditorOptions.COMBO_BOX] is True:
            assert self.get_type() == PropertyTypes.TEXT

            item_options = options[EditorOptions.COMBO_BOX_OPTIONS]
            assert isinstance(item_options, list) and len(item_options) > 0
            for item in item_options:
                assert isinstance(item, str) and len(item) > 0
            self._editor_options[EditorOptions.COMBO_BOX_OPTIONS] = copy.copy(
                item_options
            )

        elif self.get_type() in [PropertyTypes.INTEGER, PropertyTypes.REAL_NUMBER]:
            self._editor_options[EditorOptions.NUMBER_SLIDER_EDITOR] = check_dict_value(
                options, EditorOptions.NUMBER_SLIDER_EDITOR, bool, True
            )
            self._editor_options[
                EditorOptions.NUMBER_SPINNER_EDITOR
            ] = check_dict_value(
                options, EditorOptions.NUMBER_SPINNER_EDITOR, bool, True
            )

            type_to_check = int if self.get_type() == PropertyTypes.INTEGER else float
            for key in [
                EditorOptions.NUMBER_MININUM_VALUE,
                EditorOptions.NUMBER_MAXIMUM_VALUE,
                EditorOptions.NUMBER_STEP_VALUE,
            ]:
                self._editor_options[key] = get_dict_value(
                    options, key, type_to_check, None
                )

            if self.get_type() == PropertyTypes.REAL_NUMBER:
                for key in [
                    EditorOptions.NUMBER_PRECISION,
                ]:
                    self._editor_options[key] = get_dict_value(options, key, int, None)

        elif self.get_type() == PropertyTypes.TEXT:
            for key in [EditorOptions.TEXT_MIN_SIZE, EditorOptions.TEXT_MAX_SIZE]:
                self._editor_options[key] = get_dict_value(options, key, int, None)

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> str:
        return self._id

    def set_value(self, value: Any, **kargs) -> bool:
        """
        Parameters
        ==========
        value: value to set
        **kargs:
            - validation_function: a function(value) -> bool to validate the value to be set
            - trigger_event: trigger event on_property_changed and the value changes
        """

        if value is None:
            if self._can_be_null is False:
                self._listener.on_message(
                    "ERROR", "Property Item %s cannot be null." % self._name
                )
                return False

        validation_function: Optional[Callable[[Any], bool]] = kargs.get(
            "validation_function", None
        )
        if validation_function is not None and validation_function(value) is False:
            self._listener.on_message(
                "ERROR", "Invalid value for property '%s'." % self.get_name()
            )
            return False

        self._value = value

        trigger_event: Optional[bool] = kargs.get("trigger_event", True)
        if trigger_event:
            self._listener.on_property_item_changed(self)

        trigger_specific_event: Optional[bool] = kargs.get(
            "trigger_specific_event", True
        )
        if trigger_specific_event and self._specific_listener is not None:
            self._specific_listener.on_property_item_changed(self)

        return True

    def get_value(self) -> Any:
        return self._value

    def is_array(self) -> bool:
        return self._is_array

    def array_dimension(self) -> Any:
        if self._array_dimension is None:
            return None
        return tuple(self._array_dimension)

    def get_type(self) -> str:
        return self._type

    def set_is_editable(self, value: bool) -> None:
        self._editor_options[EditorOptions.EDITABLE] = value

    def is_editable(self) -> bool:
        return self._editor_options[EditorOptions.EDITABLE]

    def get_editor_options(self) -> Dict[str, Any]:
        return copy.deepcopy(self._editor_options)  # force read-only

    def get_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = dict()
        out["name"] = self._name
        out["id"] = self._id
        out["value"] = copy.deepcopy(self._value)

        options: dict = dict()
        out["options"] = options

        options[BasicOptions.TYPE] = self._type
        options[BasicOptions.CAN_BE_NULL] = self._can_be_null
        options[BasicOptions.IS_ARRAY] = self._is_array
        options[BasicOptions.ARRAY_DIMENSION] = copy.copy(self._array_dimension)
        options[BasicOptions.DEFAULT_VALUE] = copy.deepcopy(self._default_value)

        for key in self._editor_options:
            options[key] = copy.copy(self._editor_options[key])

        return out


class PropertyGroupModel:
    def __init__(
        self,
        listener: PropertyModelListener,
        params: Dict[str, Any],
    ) -> None:
        assert isinstance(listener, PropertyModelListener)
        assert isinstance(params, dict)
        assert isinstance(params["id"], str) and len(params["id"]) > 0
        assert isinstance(params["name"], str) and len(params["name"]) > 0
        assert isinstance(params["options"], dict)
        options = params["options"]

        self._listener: PropertyModelListener = listener
        self._name: str = params["name"]
        self._id: str = params["id"]
        self._items: List[Union[PropertyGroupModel, PropertyItemModel]] = list()
        assert get_dict_value(options, BasicOptions.GROUP, bool, False) is True

        if "items" in params and isinstance(params["items"], list):
            for item_params in params["items"]:
                self._add_item_by_params_dict(item_params)

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> str:
        return self._id

    def _add_item_by_params_dict(
        self,
        params: Dict[str, Any],
    ) -> Optional[Union["PropertyGroupModel", "PropertyItemModel"]]:
        item: Optional[Union["PropertyGroupModel", "PropertyItemModel"]] = None
        options = params["options"]
        if get_dict_value(options, BasicOptions.GROUP, bool, False) is True:
            item = PropertyGroupModel(self._listener, params)
            self._items.append(item)
        else:
            item = PropertyItemModel(self._listener, params)
            self._items.append(item)
        return item

    def get_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = dict()

        out["name"] = self._name
        out["id"] = self._id
        out["options"] = {BasicOptions.GROUP: True}

        items: List[dict] = list()
        out["items"] = items

        for item in self._items:
            items.append(item.get_dict())

        return out

    def get_items(self) -> List[Union["PropertyGroupModel", "PropertyItemModel"]]:
        return self._items

    def get_property_items(self) -> List["PropertyItemModel"]:
        out: List["PropertyItemModel"] = list()
        for item in self._items:
            if isinstance(item, PropertyGroupModel):
                out += item.get_property_items()
            else:
                out.append(item)
        return out

    def get_sub_groups(self) -> List["PropertyGroupModel"]:
        out: List["PropertyGroupModel"] = list()

        for item in self._items:
            if isinstance(item, PropertyGroupModel):
                out.append(item)
                out += item.get_sub_groups()

        return out


class PropertyModel:
    """
    TODO check duplicated names over the model
    """

    def __init__(self, listener: PropertyModelListener, params: dict) -> None:
        assert isinstance(listener, PropertyModelListener)
        assert isinstance(params["property_model"], list)

        self._listener: PropertyModelListener = listener
        self._items: List[PropertyGroupModel] = list()
        self._property_items: List[PropertyItemModel] = list()  # faster iteration

        for params in params["property_model"]:
            item = PropertyGroupModel(listener, params)
            self._items.append(item)

        self.get_property_items(True)

    def get_items(self) -> List[PropertyGroupModel]:
        return self._items

    def get_property_items(self, update=True) -> List[PropertyItemModel]:
        if update:
            self._property_items = list()
            for item in self._items:
                self._property_items += item.get_property_items()
        return self._property_items

    def set_value_by_property_id(self, property_id: str, value: Any, **kargs) -> bool:
        assert isinstance(property_id, str) and len(property_id) > 0
        item: Optional[PropertyItemModel] = None
        for item_prop in self._property_items:
            if item_prop.get_id() == property_id:
                item = item_prop

        if item is None:
            self._listener.on_message("ERROR", "Item %s not found." % property_id)
            return False

        return item.set_value(value, **kargs)

    def get_item_by_id(
        self, item_id: str
    ) -> Optional[Union[PropertyItemModel, PropertyGroupModel]]:
        assert isinstance(item_id, str) and len(item_id) > 0

        for item_group in self._items:
            if item_group.get_id() == item_id:
                return item_group

        for item_prop in self._property_items:
            if item_prop.get_id() == item_id:
                return item_prop

        return None

    def get_value_by_property_id(self, property_id: str) -> Any:
        assert isinstance(property_id, str) and len(property_id) > 0

        for item_prop in self._property_items:
            if item_prop.get_id() == property_id:
                return item_prop.get_value()

        return None

    def get_values(self) -> dict:
        out = dict()
        for item_prop in self._property_items:
            out[item_prop.get_id()] = item_prop.get_value()
        return out

    def update_values(self, values: dict, **kargs) -> None:
        for key in values:
            for item_prop in self._property_items:
                if item_prop.get_id() == key:
                    item_prop.set_value(values[key], **kargs)

    def get_model_dict(self) -> dict:
        out: dict = dict()

        out["property_model"] = list()

        for item in self._items:
            out["property_model"].append(item.get_dict())

        return out

    def save_to_json(self, file_path: str) -> bool:
        assert isinstance(file_path, str) and len(file_path) > 0

        with open(file_path, "w") as f:
            values_as_dict = self.get_model_dict()
            import json

            json.dump(values_as_dict, f, ensure_ascii=False)
            return True

        return False

    @staticmethod
    def load_from_json_file(
        listener: PropertyModelListener,
        file_path: str,
    ) -> Optional["PropertyModel"]:
        out: Union[PropertyModel, None] = None
        import json

        with open(file_path, "r", encoding="utf8") as f:
            data = json.load(f)
            out = PropertyModel(listener, data)

        return out

    @staticmethod
    def load_from_dict(
        listener: PropertyModelListener,
        data: dict,
    ) -> Optional["PropertyModel"]:
        out = PropertyModel(listener, data)
        return out

    def get_groups(self):
        out: List[PropertyGroupModel] = list()
        for item in self._items:
            if isinstance(item, PropertyGroupModel):
                out.append(item)
                out += item.get_sub_groups()
        return out

    # creators

    def create_group(
        self,
        group_id: str,
        group_name: str,
        parent_group: Optional[Union[str, PropertyGroupModel]] = None,
    ) -> Optional[PropertyGroupModel]:
        assert isinstance(group_id, str) and len(group_id) > 0
        assert isinstance(group_name, str) and len(group_name) > 0

        groups = self.get_groups()
        for group in groups:
            if group.get_id() == group_id:
                self._listener.on_message(
                    "ERROR", "Group ID '%s' already exists." % group_id
                )
                return None

        params = {"id": group_id, "name": group_name, "options": {"group": True}}

        if isinstance(parent_group, str):
            assert len(parent_group) > 0
            for group in groups:
                if group.get_id() == parent_group:
                    group._add_item_by_params_dict(params)

        elif isinstance(parent_group, PropertyGroupModel):
            group_model = parent_group._add_item_by_params_dict(params)
            if isinstance(group_model, PropertyGroupModel):
                return group_model
            return None

        group_model = PropertyGroupModel(self._listener, params)
        self._items.append(group_model)

        return group_model

    @staticmethod
    def create_basic_property_params(
        prop_id: str,
        name: str,
        prop_type: Optional[str],
        value: Any,
        options: Dict[str, Any],
    ) -> dict:
        params: dict = dict()
        params["id"] = prop_id
        params["name"] = name
        params["value"] = value

        params["options"] = dict()
        params[BasicOptions.TYPE] = prop_type
        params[BasicOptions.CAN_BE_NULL] = get_dict_value(
            options, BasicOptions.CAN_BE_NULL, bool, None
        )
        params[BasicOptions.DEFAULT_VALUE] = get_dict_value(
            options, BasicOptions.DEFAULT_VALUE, bool, None
        )
        params[BasicOptions.IS_ARRAY] = get_dict_value(
            options, BasicOptions.IS_ARRAY, bool, None
        )
        params[BasicOptions.ARRAY_DIMENSION] = get_dict_value(
            options, BasicOptions.ARRAY_DIMENSION, list, None
        )

        params[EditorOptions.EDITABLE] = get_dict_value(
            options, EditorOptions.EDITABLE, list, True
        )
        params[EditorOptions.SINGLE] = get_dict_value(
            options, EditorOptions.SINGLE, list, False
        )

        return params

    def check_property_id_exists(self, prop_id: str) -> bool:
        prop_items = self.get_property_items(False)
        for prop_item in prop_items:
            if prop_item.get_id() == prop_id:
                return True
        return False

    def create_text_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Optional[str],
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.TEXT, value, options
        )

        params[EditorOptions.TEXT_LINE_EDITOR] = get_dict_value(
            options, EditorOptions.TEXT_LINE_EDITOR, bool, True
        )
        params[EditorOptions.TEXT_MULTILINE_EDITOR] = get_dict_value(
            options, EditorOptions.TEXT_MULTILINE_EDITOR, bool, False
        )

        params[EditorOptions.TEXT_MIN_SIZE] = get_dict_value(
            options, EditorOptions.TEXT_MIN_SIZE, int, None
        )
        params[EditorOptions.TEXT_MAX_SIZE] = get_dict_value(
            options, EditorOptions.TEXT_MAX_SIZE, int, None
        )

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_integer_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: int,
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.INTEGER, value, options
        )

        params[EditorOptions.NUMBER_SPINNER_EDITOR] = get_dict_value(
            options, EditorOptions.NUMBER_SPINNER_EDITOR, bool, True
        )
        params[EditorOptions.NUMBER_SLIDER_EDITOR] = get_dict_value(
            options, EditorOptions.NUMBER_SLIDER_EDITOR, bool, False
        )

        for key in [
            EditorOptions.NUMBER_MININUM_VALUE,
            EditorOptions.NUMBER_MAXIMUM_VALUE,
            EditorOptions.NUMBER_STEP_VALUE,
        ]:
            params[key] = get_dict_value(options, key, int, None)

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_boolean_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Optional[int],
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.BOOLEAN, value, options
        )

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_REAL_NUMBER_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Optional[float],
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.REAL_NUMBER, value, options
        )

        params[EditorOptions.NUMBER_SPINNER_EDITOR] = get_dict_value(
            options, EditorOptions.NUMBER_SPINNER_EDITOR, bool, True
        )
        params[EditorOptions.NUMBER_SLIDER_EDITOR] = get_dict_value(
            options, EditorOptions.NUMBER_SLIDER_EDITOR, bool, False
        )

        for key in [
            EditorOptions.NUMBER_MININUM_VALUE,
            EditorOptions.NUMBER_MAXIMUM_VALUE,
            EditorOptions.NUMBER_STEP_VALUE,
        ]:
            params[key] = get_dict_value(options, key, float, None)

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_combobox_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Optional[str],
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.TEXT, value, options
        )

        params[EditorOptions.COMBO_BOX] = get_dict_value(
            options, EditorOptions.COMBO_BOX, bool, True
        )
        params[EditorOptions.COMBO_BOX_OPTIONS] = get_dict_value(
            options, EditorOptions.COMBO_BOX_OPTIONS, list, None
        )

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_checkbox_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Optional[str],
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.TEXT, value, options
        )

        params[EditorOptions.CHECK_BOX] = get_dict_value(
            options, EditorOptions.CHECK_BOX, bool, True
        )
        params[EditorOptions.CHECK_BOX_OPTIONS] = get_dict_value(
            options, EditorOptions.CHECK_BOX_OPTIONS, list, None
        )

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_file_path_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Optional[str],
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.TEXT, value, options
        )

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_folder_path_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Optional[str],
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        params = PropertyModel.create_basic_property_params(
            prop_id, name, PropertyTypes.TEXT, value, options
        )

        params[EditorOptions.FOLDER_PATH_EDITOR] = get_dict_value(
            options, EditorOptions.FOLDER_PATH_EDITOR, bool, True
        )

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

    def create_custom_property(
        self,
        group_model: PropertyGroupModel,
        prop_id: str,
        name: str,
        value: Any,
        options: Dict[str, Any],
    ) -> Optional[PropertyItemModel]:
        assert isinstance(group_model, PropertyGroupModel)

        if self.check_property_id_exists(prop_id):
            self._listener.on_message(
                "ERROR", "Property ID '%s' already exists." % prop_id
            )
            return None

        options["group"] = None
        params = PropertyModel.create_basic_property_params(
            prop_id, name, None, value, options
        )
        for key in options:
            params[key] = options[key]

        item = group_model._add_item_by_params_dict(params)

        if isinstance(item, PropertyItemModel):
            self.get_property_items(True)  # update property item list
            self._listener.on_property_model_changed(self)
            return item

        return None

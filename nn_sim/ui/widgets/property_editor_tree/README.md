# Property Editor Tree

TODO: rewrite with pydantic to generate the model, export to dict and json automatically


This is a tree editor whose editable properties can be set dynamically through a descriptor (dict or json file).

The descriptor is a dict with the following format:

```python

# dict format
props = {
    "property_model": [
        {
            "id": "group1",
            "name": "Group Name 1",
            "options": {
                "group": True
            },
            "items": [
                 {
                    "id": "prop1",
                    "name": "Name",
                    "value": "Robson",
                    "options": {
                        "type": "text",
                        "can_be_null": False,
                        "default_value": "Andre",
                        "is_array": False,
                        "array_dimension": None,
                        "group": False,
                        "editable": True,
                        "single": False,
                        "text_line_editor": True,
                        "text_min_size": 1,
                        "text_max_size": 100
                    }
                },
                {
                    "id": "prop_bool",
                    "name": "Boolean",
                    "value": False,
                    "options": {
                        "type": "boolean",
                        "can_be_null": False,
                        "default_value": True,
                        "boolean_true_text": "Yes",
                        "boolean_False_text": "No"
                    }
                },
                {
                    "id": "prop1232",
                    "name": "ComboBox",
                    "value": "Germany",
                    "options": {
                        "type": "text",
                        "can_be_null": False,
                        "default_value": "Germany",
                        "combo_box": True,
                        "combo_box_options": [
                            "Brazil",
                            "Germany",
                            "India",
                            "USA",
                            "France",
                            "England"
                        ]
                    }
                },
                {
                    "id": "prop2",
                    "name": "Country",
                    "value": None,
                    "options": {
                        "type": "text",
                        "can_be_null": False,
                        "default_value": [
                            "Germany"
                        ],
                        "check_box": True,
                        "check_box_options": [
                            "Brazil",
                            "Germany",
                            "India",
                            "USA",
                            "France",
                            "England"
                        ]
                    }
                },
                {
                    "id": "prop3",
                    "name": "Age",
                    "value": None,
                    "options": {
                        "type": "integer",
                        "can_be_null": False,
                        "default_value": 100,
                        "group": False,
                        "number_spinner_editor": True,
                        "number_min_value": 0,
                        "number_max_value": 200,
                        "number_step_value": 1
                    }
                },
                {
                    "id": "prop4",
                    "name": "Age",
                    "value": None,
                    "options": {
                        "type": "integer",
                        "can_be_null": False,
                        "default_value": 10,
                        "group": False,
                        "number_spinner_editor": True,
                        "number_min_value": 0,
                        "number_max_value": 200,
                        "number_step_value": 1
                    }
                },
                {
                    "id": "prop5",
                    "name": "Salary",
                    "value": None,
                    "options": {
                        "type": "real_number",
                        "can_be_null": False,
                        "default_value": 750.0,
                        "group": False,
                        "number_spinner_editor": True,
                        "number_min_value": 0.0,
                        "number_max_value": 1000.5,
                        "number_step_value": 10.5
                    }
                }
            ],
        },
    ],
}

```

The same format can be stored and loaded from a JSON file.


```python


import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    import darc.ui.helpers.pyqtguihelper as gg
    from darc.ui.resources import resources
    resources

    from darc.ui.widgets.property_editor_tree import (
        PropertyModel, PropertyModelListener, PropertyItemModel, PropertyTreeWidget
    )

except ImportError as e:
    print(e)
    exit(1)


ctx = gg.AppContext(name='ctx')
app = gg.Application(ctx=ctx)


class SimpleListener(PropertyModelListener):

    def on_property_item_changed(self, property_item_model: PropertyItemModel) -> None:
        print('LISTENER: ', property_item_model.get_id(), property_item_model.get_value(), 'PROPERTY CHANGED')

    def on_message(self, message_type: str, message: str) -> None:
        print('LISTENER:', message_type, message)

    def on_property_model_changed(self, property_model: PropertyModel) -> None:
        print('LISTENER:', property_model, 'MODEL CHANGED')


listener: SimpleListener = SimpleListener()

property_model: PropertyModel = PropertyModel.load_from_dict(
    listener,
    {
        "property_model": [
            {
                "id": "group1",
                "name": "Group Name 1",
                "options": {
                    "group": True
                },
                "items": [
                    {
                        "id": "prop_name",
                        "name": "Name",
                        "value": "Robson",
                        "options": {
                            "type": "text",
                            "can_be_null": False,
                            "default_value": "Andre",
                            "is_array": False,
                            "array_dimension": None,
                            "group": False,
                            "editable": False,
                            "single": False,
                            "text_line_editor": True,
                            "text_min_size": 1,
                            "text_max_size": 100
                        }
                    },
                    {
                        "id": "prop_bool",
                        "name": "Boolean",
                        "value": False,
                        "options": {
                            "type": "boolean",
                            "can_be_null": False,
                            "default_value": True,
                            "boolean_true_text": "Yes",
                            "boolean_False_text": "No"
                        }
                    },
                    {
                        "id": "prop1232",
                        "name": "ComboBox",
                        "value": "Germany",
                        "options": {
                            "type": "text",
                            "can_be_null": False,
                            "default_value": "Germany",
                            "combo_box": True,
                            "combo_box_options": [
                                "Brazil",
                                "Germany",
                                "India",
                                "USA",
                                "France",
                                "England"
                            ]
                        }
                    },
                    {
                        "id": "prop2",
                        "name": "Country",
                        "value": None,
                        "options": {
                            "type": "text",
                            "can_be_null": False,
                            "default_value": [
                                "Germany"
                            ],
                            "check_box": True,
                            "check_box_options": [
                                "Brazil",
                                "Germany",
                                "India",
                                "USA",
                                "France",
                                "England"
                            ]
                        }
                    },
                    {
                        "id": "prop3",
                        "name": "Age",
                        "value": None,
                        "options": {
                            "type": "integer",
                            "can_be_null": False,
                            "default_value": 100,
                            "group": False,
                            "number_spinner_editor": True,
                            "number_min_value": 0,
                            "number_max_value": 200,
                            "number_step_value": 1
                        }
                    },
                    {
                        "id": "prop4",
                        "name": "Age",
                        "value": None,
                        "options": {
                            "type": "integer",
                            "can_be_null": False,
                            "default_value": 10,
                            "group": False,
                            "number_spinner_editor": True,
                            "number_min_value": 0,
                            "number_max_value": 200,
                            "number_step_value": 1
                        }
                    },
                    {
                        "id": "prop5",
                        "name": "Salary",
                        "value": None,
                        "options": {
                            "type": "real_number",
                            "can_be_null": False,
                            "default_value": 750.0,
                            "group": False,
                            "number_spinner_editor": True,
                            "number_min_value": 0.0,
                            "number_max_value": 1000.5,
                            "number_step_value": 10.5
                        }
                    }
                ],
            },
            {
                "id": "group2",
                "name": "Group Name 2",
                "options": {
                    "group": True
                },
                "items": [
                    {
                        "id": "prop_name1",
                        "name": "Name",
                        "value": "Robson",
                        "options": {
                            "type": "text",
                            "can_be_null": False,
                            "default_value": "Andre",
                            "is_array": False,
                            "array_dimension": None,
                            "group": False,
                            "editable": False,
                            "single": False,
                            "text_line_editor": True,
                            "text_min_size": 1,
                            "text_max_size": 100
                        }
                    },

                ],
            }
        ],
    }
)

tree = PropertyTreeWidget(property_model)


def change_property_by_id():
    property_model.set_value_by_property_id('prop_name', 'Martin')


window = gg.BaseWindow.static_new(
    ctx,
    window_icon=gg.Icon('edit'),
    window_title="D'Arc Framework - Property Editor",
    window_size=(400, 600),
    layout=gg.Rows(
        gg.Button(text='Change Property', click=change_property_by_id),
        gg.NextRow,
        tree,
        align=gg.Align.Top
    ),
    show=True
)

sys.exit(app.exec())
```



# Future work and 


# LICENSE

```
Author: Joed Lopes da Silva (joedlopes at gmail.com)

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.

```

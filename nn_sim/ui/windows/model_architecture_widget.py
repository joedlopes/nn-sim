# from typing import List, Any, Union
from copy import deepcopy
from ..helpers import uihelper as dc

from ..widgets.property_editor_tree import (
    PropertyItemModel,
    PropertyModel,
    PropertyModelListener,
    PropertyTreeWidget,
)


PARAMS_ARCHITECTURE = {
    "property_model": [
        {
            "id": "group_arch",
            "name": "Network Architecture",
            "options": {"group": True},
            "items": [
                {
                    "id": "arch_n_inputs",
                    "name": "Number of inputs",
                    "value": None,
                    "options": {
                        "type": "integer",
                        "can_be_null": False,
                        "default_value": 2,
                        "group": False,
                        "number_spinner_editor": True,
                        "number_min_value": 1,
                        "number_max_value": 1024,
                        "number_step_value": 1,
                    },
                },
                {
                    "id": "arch_n_outputs",
                    "name": "Number of outputs",
                    "value": None,
                    "options": {
                        "type": "integer",
                        "can_be_null": False,
                        "default_value": 2,
                        "group": False,
                        "number_spinner_editor": True,
                        "number_min_value": 1,
                        "number_max_value": 1024,
                        "number_step_value": 1,
                    },
                },
                {
                    "id": "arch_output_activation_function",
                    "name": "Activation Function (Output)",
                    "value": "Sigmoid",
                    "options": {
                        "type": "text",
                        "can_be_null": False,
                        "default_value": "Sigmoid",
                        "combo_box": True,
                        "combo_box_options": [
                            "Identity",
                            "ReLU",
                            "Sigmoid",
                            "Step",
                            # "Tanh",
                        ],
                    },
                },
                {
                    "id": "arch_output_bias",
                    "name": "Bias",
                    "value": True,
                    "options": {
                        "type": "boolean",
                        "can_be_null": False,
                        "default_value": True,
                        "boolean_true_text": "Active",
                        "boolean_false_text": "Disabled",
                    },
                },
                {
                    "id": "arch_n_hidden",
                    "name": "Number of Hidden layers",
                    "value": None,
                    "options": {
                        "type": "integer",
                        "can_be_null": False,
                        "default_value": 0,
                        "group": False,
                        "number_spinner_editor": True,
                        "number_min_value": 0,
                        "number_max_value": 100,
                        "number_step_value": 1,
                    },
                },
                {
                    "id": "arch_loss_function",
                    "name": "Loss Function",
                    "value": "Sum of Squared Errors",
                    "options": {
                        "type": "text",
                        "can_be_null": False,
                        "default_value": "Sum of Squared Errors",
                        "combo_box": True,
                        "combo_box_options": [
                            "Sum of Squared Errors",
                            "Binary Cross Entropy Loss (log-loss)",
                            "Mean Squared Error (MSE)",
                            "Mean Absolute Error (MAE)",
                        ],
                    },
                },
            ],
        },
    ]
}

PARAMS_LAYER = {
    "property_model": [
        {
            "id": "layer_group",
            "name": "Hidden Layer",
            "options": {"group": True},
            "items": [
                {
                    "id": "layer_n_neurons",
                    "name": "Number of neurons",
                    "value": None,
                    "options": {
                        "type": "integer",
                        "can_be_null": False,
                        "default_value": 2,
                        "group": False,
                        "number_spinner_editor": True,
                        "number_min_value": 1,
                        "number_max_value": 1024,
                        "number_step_value": 1,
                    },
                },
                {
                    "id": "layer_activation_function",
                    "name": "Activation Function",
                    "value": "Sigmoid",
                    "options": {
                        "type": "text",
                        "can_be_null": False,
                        "default_value": "Sigmoid",
                        "combo_box": True,
                        "combo_box_options": [
                            "Identity",
                            "ReLU",
                            "Sigmoid",
                            "Step",
                            # "Tanh",
                        ],
                    },
                },
                {
                    "id": "layer_bias",
                    "name": "Bias",
                    "value": True,
                    "options": {
                        "type": "boolean",
                        "can_be_null": False,
                        "default_value": True,
                        "boolean_true_text": "Active",
                        "boolean_false_text": "Disabled",
                    },
                },
            ],
        },
    ]
}


class ModelArchitectureWidget(dc.QWidget, PropertyModelListener):

    on_architecture_changed = dc.Signal(object)

    def __init__(self):
        super().__init__()

        params = deepcopy(PARAMS_ARCHITECTURE)
        self.model_arch = PropertyModel(self, params)

        self.params_layers = list()
        # params = deepcopy(PARAMS_LAYER)
        self.model_layers = PropertyModel(self, dict(property_model=[]))

        self.tree_arch = PropertyTreeWidget(self.model_arch)
        self.tree_layers = PropertyTreeWidget(self.model_layers)
        self.tree_arch.setMaximumHeight(200)

        self.tree_layers.setColumnCount(2)
        self.tree_arch.setColumnCount(2)

        dc.Widget(
            widget=self,
            layout=dc.Columns(
                dc.Label("<h2>Network Architecture</h2>"),
                dc.HLine(),
                self.tree_arch,
                dc.Label("<h3>Hidden Layers</h3>"),
                dc.HLine(),
                self.tree_layers,
                align=dc.Align.Top,
            ),
        )

    def on_property_item_changed(self, property_item_model: PropertyItemModel) -> None:
        prop_id = property_item_model.get_id()
        if prop_id.startswith("arch_n_hidden"):
            self.update_hidden_layers(property_item_model.get_value())

        for key in [
            "arch",
            "bias",
            "n_hidden",
            "n_outputs",
            "n_inputs",
            "n_neurons",
        ]:
            if key in prop_id:
                self.emit_change()

    def on_message(self, message_type: str, message: str) -> None:
        print(message_type, message)

    def on_property_model_changed(self, property_model: PropertyModel) -> None:
        pass

    def update_hidden_layers(self, n_layers):
        prop_model = self.model_layers.get_model_dict()
        if len(prop_model["property_model"]) != n_layers:
            if len(prop_model["property_model"]) > n_layers:
                prop_model["property_model"] = prop_model["property_model"][:n_layers]
            else:
                while len(prop_model["property_model"]) < n_layers:
                    if len(prop_model["property_model"]) > 0:
                        prop_model["property_model"].append(
                            deepcopy(prop_model["property_model"][-1])
                        )
                    else:
                        prop_model["property_model"].append(
                            deepcopy(PARAMS_LAYER["property_model"][0])
                        )

                for idx, layer_group in enumerate(prop_model["property_model"]):
                    layer_group["id"] = f"layer_{idx:04}"
                    layer_group["name"] = f"Hidden Layer {idx}"
                    layer_group["items"][0]["id"] = f"layer_n_neurons_{idx:04}"
                    layer_group["items"][1][
                        "id"
                    ] = f"layer_activation_function_{idx:04}"
                    layer_group["items"][2]["id"] = f"layer_bias_{idx:04}"

            self.model_layers = PropertyModel(self, prop_model)
            self.tree_layers.set_property_model(self.model_layers)

    def get_model_info(self) -> dict:
        info = self.model_arch.get_values()
        info["hidden_layers"] = self.model_layers.get_values()
        print(info)
        return info

    def emit_change(self) -> None:
        self.on_architecture_changed.emit(self.get_model_info())

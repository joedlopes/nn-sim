from typing import Optional
from ..helpers import uihelper as dc

from ...data.dataset_loader import DatasetNN


class TrainWidget(dc.QWidget):

    def __init__(self):
        super().__init__()

        self.btn_start_train = dc.Button("Start Training")

        self.sp_lr = dc.DoubleSpinBox(value=0.1, single_step=0.001, decimals=6)
        self.sp_lr.setMinimum(1e-6)
        self.sp_lr.setMaximum(1e3)
        self.sp_lr.setValue(1e-2)
        self.cb_optim = dc.ComboBox(
            selected_item="SGD",
            items=[
                "SGD",
                "SGD with Momentum",
                "ADAM",
                "RMSprop",
            ],
        )

        self.cb_batch_mode = dc.ComboBox(selected_item="Mini Batch", items=["Mini Batch", "Single Batch (all samples)"], on_index_changed=self.batch_mode_changed)
        self.sp_batch_size = dc.SpinBox(range=(1, 100), value=100, single_step=1)
        self.max_batch_size = 100

        dc.Widget(
            widget=self,
            window_ops=dc.WindowOps(title="Train", size=(200, 200)),
            layout=dc.Columns(
                self.btn_start_train,
                dc.Label("Learning Rate:"),
                self.sp_lr,
                dc.Label("Batch Mode:"),
                self.cb_batch_mode,
                dc.Label("Batch Size:"),
                self.sp_batch_size,
                dc.Label("Optimizer"),
                self.cb_optim,
                align=dc.Align.Top,
            )
        )

    def on_dataset_changed(self, dataset: DatasetNN) -> None:
        self.max_batch_size = len(dataset)
        self.sp_batch_size.setMaximum(self.max_batch_size)
        self.sp_batch_size.setValue(self.max_batch_size)

    def batch_mode_changed(self, arg1=None) -> None:
        if self.cb_batch_mode.currentText() == "Mini Batch":
            self.sp_batch_size.setEnabled(True)
        else:
            self.sp_batch_size.setValue(self.max_batch_size)
            self.sp_batch_size.setEnabled(False)

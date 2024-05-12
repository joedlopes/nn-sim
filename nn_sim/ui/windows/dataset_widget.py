from ..helpers import uihelper as dc

from ...data.dataset_loader import DatasetNN


class DatasetWidget(dc.QWidget):

    on_dataset_changed = dc.Signal(object)

    def __init__(self):
        super().__init__()

        self.txt_name = dc.Label("<b>Name:</b>")
        self.txt_n_inputs = dc.Label("<b>Number of Inputs:</b>")
        self.txt_n_outputs = dc.Label("<b>Number of Outputs:</b>")
        self.txt_n_samples = dc.Label("<b>Number of Samples:</b>")

        dc.Widget(
            widget=self,
            layout=dc.Columns(
                dc.Label("<h2>Dataset:</h2>"),
                dc.Button("Select Dataset", on_click=self.select_dataset),
                self.txt_name,
                self.txt_n_inputs,
                self.txt_n_outputs,
                self.txt_n_samples,
                align=dc.Align.Top,
            ),
        )
        self.dataset: DatasetNN | None = None

    def select_dataset(self, file_path: str | None = None) -> None:
        if file_path is not None:
            file_path = dc.OpenFile("Selecte dataset file",
                                    "nn_sim dataset (*.nnset);;All Files(*)")

        if not file_path:
            return

        self.dataset = DatasetNN(file_path)

        self.txt_name.setText(f"<b>Name:</b> {self.dataset.dataset_name}")
        self.txt_n_inputs.setText(f"<b>Number of Inputs:</b> {self.dataset.X.shape[1]}")
        self.txt_n_outputs.setText(f"<b>Number of Outputs:</b> {self.dataset.Y.shape[1]}")
        self.txt_n_samples.setText(f"<b>Number of Outputs:</b> {self.dataset.X.shape[0]}")
        
        self.on_dataset_changed(self.dataset)

from ..helpers import uihelper as dc

from ...data.dataset_loader import DatasetNN


class DatasetWidget(dc.QWidget):

    on_dataset_changed = dc.Signal(object)
    on_sample_changed = dc.Signal(object)

    def __init__(self):
        super().__init__()

        self.txt_name = dc.Label("<b>Name:</b>")
        self.txt_n_inputs = dc.Label("<b>Number of Inputs:</b>")
        self.txt_n_outputs = dc.Label("<b>Number of Outputs:</b>")
        self.txt_n_samples = dc.Label("<b>Number of Samples:</b>")

        self.txt_current_sample = dc.Label("0")
        self.btn_next_sample = dc.Button("Next >", on_click=self.next_sample)
        self.btn_prev_sample = dc.Button("< Previous", on_click=self.prev_sample)
        self.sample_index = 0

        dc.Widget(
            widget=self,
            layout=dc.Columns(
                dc.Label("<h2>Dataset:</h2>"),
                dc.Button("Select Dataset", on_click=self.select_dataset),
                self.txt_name,
                self.txt_n_inputs,
                self.txt_n_outputs,
                self.txt_n_samples,
                dc.HLine(),
                dc.Label("<b>Selected Sample:</b>"),
                self.txt_current_sample,
                dc.Rows(self.btn_prev_sample, self.btn_next_sample),
                align=dc.Align.Top,
            ),
        )
        self.dataset: DatasetNN | None = None

    def prev_sample(self) -> None:
        if self.dataset is None:
            return
        self.sample_index -= 1
        self.sample_index = max(0, self.sample_index)
        self.on_sample_changed.emit(self.sample_index)
        self.txt_current_sample.setText(f"{self.sample_index}")

    def next_sample(self) -> None:
        if self.dataset is None:
            return
        self.sample_index += 1
        self.sample_index = min(len(self.dataset) - 1, self.sample_index)
        self.on_sample_changed.emit(self.sample_index)
        self.txt_current_sample.setText(f"{self.sample_index}")

    def select_dataset(self, file_path: str | None = None) -> None:
        print("select dataset", file_path)
        if not file_path:
            file_path = dc.OpenFile(
                "Select dataset file", "nn_sim dataset (*.nnset);;All Files(*)"
            )

        if not file_path:
            return

        self.dataset = DatasetNN(file_path)

        self.txt_name.setText(f"<b>Name:</b> {self.dataset.dataset_name}")
        self.txt_n_inputs.setText(f"<b>Number of Inputs:</b> {self.dataset.X.shape[1]}")
        self.txt_n_outputs.setText(
            f"<b>Number of Outputs:</b> {self.dataset.Y.shape[1]}"
        )
        self.txt_n_samples.setText(
            f"<b>Number of Outputs:</b> {self.dataset.X.shape[0]}"
        )

        self.on_dataset_changed.emit(self.dataset)

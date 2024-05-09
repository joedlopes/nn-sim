import numpy as np


class Dataset:

    def __init__(self) -> None:
        self._X: np.ndarray
        self._Y: np.ndarray

    def __len__(self) -> int:
        raise NotImplementedError

    def __getitem__(self, index: int) -> tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError

    @property
    def X(self) -> np.ndarray:
        """input samples array (N, m)"""
        return self._X

    @property
    def Y(self) -> np.ndarray:
        """output samples array (N, c)"""
        return self._Y


class DatasetNN(Dataset):

    def __init__(
        self,
        file_path: str,
        *,
        dtype_inputs: np.dtype = np.float64,
        dtype_outputs: np.dtype = np.float64,
    ) -> None:
        super().__init__()

        self.file_path: str = file_path
        self.dataset_name: str
        self.input_names: list[str]
        self.output_names: list[str]
        self._X: np.ndarray
        self._Y: np.ndarray
        self._load(dtype_inputs, dtype_outputs)

    def _load(
        self,
        dtype_inputs: np.dtype = np.float64,
        dtype_outputs: np.dtype = np.float64,
    ):

        with open(self.file_path, "r") as fp:
            lines = fp.readlines()

            self.dataset_name = lines[0].rstrip()
            num_inputs = int(lines[1].rstrip())
            self.input_names = [name for name in lines[1].rstrip().split(",")]
            num_outputs = int(lines[3].rstrip())
            self.output_names = [name for name in lines[4].rstrip().split(",")]

            inputs = []
            outputs = []

            for row, line in enumerate(lines[5:]):
                x, y = [p.strip() for p in line.rstrip().split(";")]

                x = [v.strip() for v in x.split(",")]
                y = [v.strip() for v in y.split(",")]

                x = [float(v) for v in x if len(x) > 0]
                y = [float(v) for v in y if len(x) > 0]

                assert (
                    len(x) == num_inputs
                ), f"Error in row {row}: invalid number of inputs."
                assert (
                    len(y) == num_outputs
                ), f"Error in row {row}: invalid number of outputs."

                inputs.append(x)
                outputs.append(y)

            self._X = np.array(inputs, dtype=dtype_inputs)
            self._Y = np.array(outputs, dtype=dtype_outputs)

    def __len__(self) -> int:
        return len(self._X)

    def __getitem__(self, index: int) -> tuple[np.ndarray, np.ndarray]:
        x = self._X[index]
        y = self._Y[index]
        return x, y

    def __str__(self) -> str:
        return f"DatasetNN ({self.dataset_name}: Input Shape({self.X.shape}); Output Shape{self.Y.shape})"


class DataLoader:

    def __init__(
        self,
        dataset: Dataset,
        batch_size: int = 0,
        shuffle: bool = True,
    ) -> None:
        self.dataset = dataset
        self.batch_size: int = batch_size
        self.shuffle: bool = shuffle

        if batch_size <= 0:
            self.batch_size = len(self.dataset)

        self.num_splits: int = round(len(self.dataset) / self.batch_size)
        self.indexes = np.arange(len(self.dataset), dtype=np.int64)

    def __iter__(self):

        indexes = self.indexes
        if self.shuffle:
            indexes = np.random.shuffle(indexes)

        for batch_idx in range(0, len(self.dataset), self.batch_size):
            X = []
            Y = []

            for sample_idx in range(
                batch_idx, min(len(dataset), batch_idx + self.batch_size)
            ):
                x, y = dataset[sample_idx]
                X.append(x)
                Y.append(y)

            yield np.array(X), np.array(Y)

    def __len__(self) -> int:
        return self.num_splits


if __name__ == "__main__":
    from tqdm import tqdm

    dataset = DatasetNN(
        "./datasets/iris.nnset",
        dtype_inputs=np.float32,
        dtype_outputs=np.int64,
    )

    print(dataset)

    for idx in range(0, len(dataset), 20):
        x, y = dataset[idx]
        print(x, y)

    loader = DataLoader(dataset, 5, shuffle=True)
    for X, Y in tqdm(loader):
        print(X)
        print(Y)

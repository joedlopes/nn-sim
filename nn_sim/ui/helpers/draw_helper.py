#
# Author: Joed Lopes da Silva
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


from typing import Tuple, Union
import numpy as np


class BaseDrawHelper:
    """Interface for implementing basic drawer functions"""

    def reset(self, update: bool = True) -> None:
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError

    def point(
        self,
        x: float,
        y: float,
        z: float,
        color: Tuple[float, float, float] = (0, 1, 0, 1),
        point_size: float = 0.05,
        update: bool = True,
    ) -> None:
        raise NotImplementedError

    def points(
        self,
        points: np.ndarray,
        colors: Union[Tuple[float, float, float, float], np.ndarray] = (
            0.0,
            1.0,
            0.0,
            1.0,
        ),
        points_size: float = 0.05,
        update: bool = True,
    ) -> None:
        raise NotImplementedError

    def line(
        self,
        p1: Tuple[float, float, float],
        p2: Tuple[float, float, float],
        color: Tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
        line_width: float = 1.0,
        update: bool = True,
    ) -> None:
        raise NotImplementedError

    def lines(
        self,
        line_pts: np.ndarray,
        colors: Tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
        line_width: float = 1.0,
        update: bool = True,
    ) -> None:
        raise NotImplementedError

    def text(
        self,
        x: float,
        y: float,
        z: float,
        text: str,
        text_size: float = 10.0,
        text_color: Tuple[float, float, float, float] = (0.0, 1.0, 0.0, 1.0),
        update: bool = True,
    ) -> None:
        raise NotImplementedError

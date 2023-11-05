from __future__ import annotations
from abc import ABC, abstractmethod
import base64
from pathlib import Path
import numpy as np
import cv2


class StateContainer(ABC):
    """A container for state that can be serialized to/from a json-safe dict."""

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, d: dict):
        return cls(**d)

    def __str__(self):
        return str(self.to_dict())


class ImageContainer(StateContainer):
    data: np.ndarray
    shape: tuple[int, ...]

    def __init__(self, data: np.ndarray):
        self.data = data
        self.shape = data.shape

        assert len(self.shape) == 2 or (
            len(self.shape) == 3 and self.shape[2] == 3
        ), "Image must be 2D or 3D RGB"

    def to_dict(self):
        data_msg = base64.b64encode(self.data.tobytes()).decode("utf-8")
        return dict(data=data_msg, shape=self.shape)

    @classmethod
    def from_file(cls, path: str | Path):
        path = Path(path).expanduser()
        data = cv2.imread(str(path))
        return cls(data)

    @classmethod
    def from_dict(cls, d: dict):
        data_msg = base64.b64decode(d["data"])
        data = np.frombuffer(data_msg, dtype=np.uint8).reshape(*d["shape"])
        return cls(data)

    def __str__(self):
        return f"Image(shape={self.shape})"

from functools import reduce
import operator
import struct
from typing import BinaryIO, Sequence

import numpy as np
import numpy.typing as npt
from numba import njit
import torch
from torch import nn

from neural_network.features.feature_set import FeatureSet

VERSION = 0x7AF32F20
DEFAULT_DESCRIPTION = "Network trained with the https://github.com/official-stockfish/nnue-pytorch trainer."

class NNUEWriter:
    """
    Serialize NNUE models into Stockfish-compatible .nnue format.
    """

    def __init__(self, model, description: str = DEFAULT_DESCRIPTION):
        self.model = model
        self.description = description
        self.buffer = bytearray()

    def write(self, file_path: str):
        """Write the serialized model to a file."""
        with open(file_path, "wb") as f:
            f.write(self.buffer)

    def serialize(self):
        """Serialize the model into the buffer."""
        self._write_header()
        self._write_layers()

    def _write_header(self):
        """Write the header information."""
        self._write_int32(VERSION)
        self._write_string(self.description)

    def _write_layers(self):
        """Write the layers of the model."""
        for layer in self.model.model:
            if isinstance(layer, nn.Linear):
                self._write_tensor(layer.weight.data)
                self._write_tensor(layer.bias.data)

    def _write_int32(self, value: int):
        self.buffer.extend(struct.pack("<I", value))

    def _write_string(self, value: str):
        encoded = value.encode("utf-8")
        self._write_int32(len(encoded))
        self.buffer.extend(encoded)

    def _write_tensor(self, tensor: torch.Tensor):
        """Write a tensor to the buffer."""
        array = tensor.cpu().numpy()
        self.buffer.extend(array.tobytes())


class NNUEReader:
    """
    Deserialize Stockfish-compatible .nnue models.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self):
        """Read and deserialize the model from a file."""
        with open(self.file_path, "rb") as f:
            self.buffer = f.read()
        return self._deserialize()

    def _deserialize(self):
        """Deserialize the model from the buffer."""
        version = self._read_int32()
        if version != VERSION:
            raise ValueError("Unsupported version: {}".format(version))
        description = self._read_string()
        print("Model description:", description)
        # Placeholder: Reconstruct the NNUE model here.
        return None  # Update this line to reconstruct the model as needed

    def _read_int32(self) -> int:
        value = struct.unpack("<I", self.buffer[:4])[0]
        self.buffer = self.buffer[4:]
        return value

    def _read_string(self) -> str:
        length = self._read_int32()
        value = self.buffer[:length].decode("utf-8")
        self.buffer = self.buffer[length:]
        return value
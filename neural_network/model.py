from typing import Generator

import torch
from torch import nn, Tensor
import torch.nn.functional as F
from neural_network.features.feature_set import FeatureSet
from neural_network.serialize import NNUEWriter, NNUEReader

class StackedLinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, count: int):
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features
        self.count = count
        self.linear = nn.Linear(in_features, out_features * count)

        self._init_uniformly()

    @torch.no_grad()
    def _init_uniformly(self) -> None:
        init_weight = self.linear.weight[0 : self.out_features, :]
        init_bias = self.linear.bias[0 : self.out_features]

        self.linear.weight.copy_(init_weight.repeat(self.count, 1))
        self.linear.bias.copy_(init_bias.repeat(self.count))

    def forward(self, x: Tensor, ls_indices: Tensor) -> Tensor:
        stacked_output = self.linear(x)

        return self.select_output(stacked_output, ls_indices)

    def select_output(self, stacked_output: Tensor, ls_indices: Tensor) -> Tensor:
        reshaped_output = stacked_output.reshape(-1, self.out_features)

        idx_offset = torch.arange(
            0,
            ls_indices.shape[0] * self.count,
            self.count,
            device=stacked_output.device,
        )
        indices = ls_indices.flatten() + idx_offset

        selected_output = reshaped_output[indices]

        return selected_output

class NNUEModel(nn.Module):
    def __init__(
        self,
        input_size: int,
        hidden_sizes: list[int],
        output_size: int,
        feature_set: FeatureSet = None,
    ):
        super().__init__()

        self.feature_set = feature_set
        layers = []
        current_size = input_size

        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(current_size, hidden_size))
            layers.append(nn.ReLU())
            current_size = hidden_size

        layers.append(nn.Linear(current_size, output_size))

        self.model = nn.Sequential(*layers)

    def forward(self, x: Tensor) -> Tensor:
        if self.feature_set:
            x = self.feature_set.get_active_features(x)
        return self.model(x)

    def initialize_weights(self):
        """Initialize weights to match Stockfish NNUE expectations."""
        for layer in self.model:
            if isinstance(layer, nn.Linear):
                nn.init.uniform_(layer.weight, -0.01, 0.01)
                nn.init.constant_(layer.bias, 0)

    def save(self, file_path: str):
        """Save the model to a file."""
        torch.save(self.state_dict(), file_path)

    @staticmethod
    def load(file_path: str, input_size: int, hidden_sizes: list[int], output_size: int):
        """Load the model from a file."""
        model = NNUEModel(input_size, hidden_sizes, output_size)
        model.load_state_dict(torch.load(file_path))
        return model

    def save_stockfish_format(self, file_path: str):
        """Save the model in Stockfish-compatible .nnue format."""
        writer = NNUEWriter(self)
        writer.serialize()
        writer.write(file_path)

    @staticmethod
    def load_stockfish_format(file_path: str):
        """Load a Stockfish-compatible .nnue model."""
        reader = NNUEReader(file_path)
        return reader.read()


def generate_stockfish_nn():
    """Generate a Stockfish-compatible NNUE model with predefined hidden layers."""
    input_size = 512  # HalfKP input size
    hidden_sizes = [256, 32]  # Stockfish NNUE hidden layers
    output_size = 1
    return NNUEModel(input_size, hidden_sizes, output_size)


def generate_nn_from_config(config_path: str):
    """Generate a neural network model based on a user-defined configuration.

    Args:
        config_path (str): Path to the configuration file specifying hidden layers.

    Returns:
        NNUEModel: A PyTorch model with the Stockfish NNUE input/output layers and user-defined hidden layers.
    """
    import json

    # Load configuration
    with open(config_path, "r") as f:
        config = json.load(f)

    input_size = 512  # HalfKP input size
    hidden_layers = config.get("hidden_layers", [256, 128])  # Default hidden layers
    output_size = 1

    return NNUEModel(input_size, hidden_layers, output_size)

def mutate_model(model: NNUEModel, temperature: float) -> NNUEModel:
    """Mutate a model by slightly tuning a few nodes based on a temperature variable.

    Args:
        model (NNUEModel): The base model to mutate.
        temperature (float): Controls the extent of mutation. Higher values increase the number of nodes changed and the magnitude of changes.

    Returns:
        NNUEModel: A new mutated model.
    """
    import copy

    # Clone the model to avoid modifying the original
    mutated_model = copy.deepcopy(model)

    for layer in mutated_model.model:
        if isinstance(layer, nn.Linear):
            # Determine the number of nodes to mutate based on temperature
            num_nodes_to_mutate = max(1, int(temperature * layer.weight.size(0)))

            # Randomly select nodes to mutate
            node_indices = torch.randperm(layer.weight.size(0))[:num_nodes_to_mutate]

            # Apply mutations to the selected nodes
            for idx in node_indices:
                layer.weight.data[idx] += torch.randn_like(layer.weight.data[idx]) * temperature
                layer.bias.data[idx] += torch.randn_like(layer.bias.data[idx]) * temperature

    return mutated_model

def breed_models(parent1: NNUEModel, parent2: NNUEModel) -> NNUEModel:
    """Breed two parent models by averaging their weights and biases.

    Args:
        parent1 (NNUEModel): The first parent model.
        parent2 (NNUEModel): The second parent model.

    Returns:
        NNUEModel: A new model created by averaging the weights and biases of the parents.
    """
    import copy

    # Ensure both parents have the same architecture
    if len(parent1.model) != len(parent2.model):
        raise ValueError("Parent models must have the same architecture.")

    # Clone the first parent to create the child model
    child_model = copy.deepcopy(parent1)

    for layer1, layer2, child_layer in zip(parent1.model, parent2.model, child_model.model):
        if isinstance(layer1, nn.Linear) and isinstance(layer2, nn.Linear):
            # Average the weights and biases of the two parents
            child_layer.weight.data = (layer1.weight.data + layer2.weight.data) / 2
            child_layer.bias.data = (layer1.bias.data + layer2.bias.data) / 2

    return child_model